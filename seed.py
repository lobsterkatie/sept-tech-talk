from model import Search, db, connect_to_db
from server import app
from game import do_searches, LEGAL_WORDS

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

        #make sure both words are legal; if either isn't, add it to the more_words
        #file and print an error to the console
        #(this is based on the assumption that the seed file is hand-curated and
        #therefore that any words missing from LEGAL_WORDS shouldn't be)
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

        #if we've made it to here, this is a new pair, so run the search and add
        #the results to the database if a path is found
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


def seed_words():
    """Add words to the DB, including their degree. Based on usr/share/dict
       word list"""


seed_pairs()
