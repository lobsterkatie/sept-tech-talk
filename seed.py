from model import Search, Word, db, connect_to_db
from server import app
from game import do_searches, LEGAL_WORDS
from itertools import product

connect_to_db(app)


def seed_pairs():
    """Seed the DB with the word pairs in seed_pairs.txt"""

    with open("seed_pairs.txt") as seed_file:
        pairs = [line.strip().split(" ") for line in seed_file if line != "\n"]

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
        results = do_searches(start_word, end_word, 1000)
        if results:
            print "PATH FOUND: (", start_word, end_word, ")"
            dfs_result = Search(**results["DFS"])
            bfs_result = Search(**results["BFS"])
            db.session.add_all([dfs_result, bfs_result])
            db.session.commit()
            pairs_added += 1
        #if a path isn't found, add the pair to unconnected.txt
        else:
            print "NO PATH FOUND: (", start_word, end_word, ")"
            with open("unconnected.txt", "a") as unconnected_words_file:
                unconnected_words_file.write(start_word + " " + end_word + "\n")

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



seed_pairs()

# note: these take a loooooong time to run - uncomment with care
# seed_words()
# seed_words(update=True)
