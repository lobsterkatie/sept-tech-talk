from model import Search, Word, db
from game import do_searches, LEGAL_WORDS
from itertools import product
from random import sample
from sqlalchemy.sql.functions import char_length


def seed_pairs(num_trials, pairs=None):
    """Seed the DB either with the word pairs given or with the word pairs
       in seed_pairs.txt. For each pair, run num_trials trials."""

    if not pairs:
        with open("seed_pairs.txt") as seed_file:
            pairs = [line.strip().split(" ")
                     for line in seed_file
                     if line != "\n"]

    pairs_added = 0

    for start_word, end_word in pairs:

        #create a way to pause in between pairs of words
        print "\n\nabout to do (", start_word, end_word, ")"
        # import pdb; pdb.set_trace()

        #make sure both words are legal; if either isn't, add it to the
        #more_words file and print an error to the console
        #(this is based on the assumption that the seed file is hand-curated
        #and therefore that any words missing from LEGAL_WORDS shouldn't be)
        illegal_words = set([start_word, end_word]) - LEGAL_WORDS
        if illegal_words:
            with open("more_words.txt", "a") as more_words_file:
                for word in illegal_words:
                    more_words_file.write(word + "\n")
                    print "\n\nADDED", word, "TO MORE_WORDS.TXT"
                print "\n\nPLEASE RESTART SEED.PY"


        #see if this search has already been done; if so, skip this pair
        prev_result = (Search.query.filter(Search.start_word == start_word,
                                           Search.end_word == end_word)
                                   .all())
        if prev_result:
            print "ALREADY IN DATABASE: (", start_word, end_word, ")"
            continue

        #if we've made it to here, this is a new pair, so run the search and
        #add the results to the database if a path is found
        results = do_searches(start_word, end_word, num_trials)
        if results:
            print "PATH FOUND: (", start_word, end_word, ")"
            dfs_result = Search(**results["DFS"])
            bfs_result = Search(**results["BFS"])
            db.session.add_all([dfs_result, bfs_result])
            db.session.commit()
            pairs_added += 1
        #if a path isn't found, and we're seeding custom-curated pairs, add
        #the pair to unconnected.txt
        else:
            print "NO PATH FOUND: (", start_word, end_word, ")"
            if not pairs:
                with open("unconnected.txt", "a") as unconnected_words_file:
                    unconnected_words_file.write(
                        start_word + " " + end_word + "\n")

    print "\n\nPAIRS ADDED:", pairs_added


def seed_words(update=False, words_to_add=None):
    """Add words to the DB, including their degree. Based on usr/share/dict
       word list, with some additions"""

    #for use later
    LETTERS = list("abcdefghijklmnopqrstuvwxyz")

    words_added = words_updated = 0

    if not words_to_add:
        words_to_add = LEGAL_WORDS

    for i, word in enumerate(words_to_add):

        #provide a sense of progress
        if i % 100 == 0:
            print i, word

        #check if the word is already in the database
        word_in_DB = Word.query.filter(Word.word == word).first()

        #if we're not updating degrees, but merely adding words to the DB,
        #only deal with the word if it's new (not already in the DB)
        if not update and word_in_DB:
            continue

        #if we get to here, either it's a new word or we're updating degrees
        #in either case, calculate the degree

        #create an accumulator to count the degree
        degree = 0
        connections = []

        #store the word as a list of characters for easy substitution
        word_letters = list(word)

        #try each letter of the alphabet in each position
        for i, substitute_letter in product(range(len(word)), LETTERS):

            #substitute the current letter into the current position in a
            #copy of the word
            potential_new_word_letters = word_letters[:]
            potential_new_word_letters[i] = substitute_letter

            #turn that into a string, and see if it's legal
            #if so, increment the degree
            potential_new_word = "".join(potential_new_word_letters)
            if (potential_new_word in LEGAL_WORDS and
                potential_new_word != word):
                degree += 1
                connections.append(potential_new_word)

        #now that we know the word's degree, either add it to the DB (if it's
        #new) or update the degree (if it's changed)
        if not word_in_DB:
            print "ADDING", word, degree, connections
            new_DB_word = Word(word=word, degree=degree)
            db.session.add(new_DB_word)
            words_added += 1
        elif word_in_DB.degree != degree:
            print "UPDATING", word, word_in_DB.degree, "->", degree
            word_in_DB.degree = degree
            words_updated += 1
        db.session.commit()

    print "\n\nWORDS ADDED:", words_added
    print "\n\nWORDS UPDATED:", words_updated


def make_random_pairs(min_word_length,
                      max_word_length,
                      num_pairs_per_word_length):
    """Come up with random pairs to test. Returns a set of tuples."""

    pairs = set()

    #create num_pairs for each requested word length
    for word_length in range(min_word_length, max_word_length + 1):

        #get all non-island (degree >= 1) words of the current length out of
        #the database
        words = (Word.query.filter(char_length(Word.word) == word_length,
                                   Word.degree != 0)
                           .all())

        #grab num_pairs random pairs of them and add them to our set
        for _ in range(num_pairs_per_word_length):
            pairs.add(tuple([word.word for word in sample(words, 2)]))


    return pairs



if __name__ == "__main__":

    #if we're running this file directly (which, to be fair, we always should
    #be), create a fake Flask app so we can talk to the database
    from flask import Flask
    from model import connect_to_db
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."


    #uncomment any of the following to run them
    #note that the functions seeding words take a loooooong time to run, so
    #uncomment them with care

    #to add curated pairs to the database
    # seed_pairs(num_trials=1000)

    #to add random pairs to the database
    # pairs = make_random_pairs(11, 16, 100)
    # seed_pairs(num_trials=1, pairs=pairs)

    #to add new words to the database
    # seed_words()

    #to update the degrees of all words after new words have been added
    # seed_words(update=True)
