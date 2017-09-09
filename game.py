from data_structs import Stack, Queue
from random import shuffle, randint
from datetime import datetime


#get set of legal words
with open("/usr/share/dict/words") as words_file:
    LEGAL_WORDS = {line.strip() for line in words_file}
with open("more_words.txt") as more_words_file:
    LEGAL_WORDS.update(line.strip() for line in more_words_file)
#remove proper nouns
LEGAL_WORDS = {word for word in LEGAL_WORDS if not word.istitle()}


###############################################################################
# WordNode class

class WordNode(object):
    """A linked list node used for storing the path from start_word to
       end_word. Each node points up, to its parent.
    """

    #make WordNodes take up less memory, since we know ahead of time all the
    #attributes they'll ever have, and we're going to be creating a lot of them
    __slots__ = ("word", "parent")


    def __init__(self, word, parent=None):
        self.word = word
        self.parent = parent


    def __repr__(self):
        """Provide helpful output when printing"""

        repr_str = "<WordNode word={word} parent={parent}>"
        return repr_str.format(word=self.word, parent=self.parent.word)


    def __eq__(self, other):
        """Allow WordNodes to be compared using =="""

        return self.word == other.word


    def __ne__(self, other):
        """Allow WordNodes to be compared using !="""

        return not self.__eq__(other)


###############################################################################
# GameRound class

class GameRound(object):
    """One round of a kids game transforming one word to another"""

    def __new__(cls, start_word, end_word):
        """Only create the GameRound if words are the same length, different
           from each other, and both legal words."""

        if len(start_word) != len(end_word):
            raise Exception("words must be the same length")
        elif start_word == end_word:
            raise Exception("words must be different")
        elif start_word not in LEGAL_WORDS or end_word not in LEGAL_WORDS:
            raise Exception("both words must be legal words")
        else:
            return super(GameRound, cls).__new__(cls)


    def __init__(self, start_word, end_word):
        self.start_word = WordNode(start_word)
        self.end_word = WordNode(end_word)
        self.word_length = len(start_word)


    def play_game(self, testing=False):
        """Play the game, printing DFS and BFS solution paths to the terminal
           if testing flag set to True.
        """

        #do DFS, and time it
        start_time = datetime.now()
        self.DFS_path_end, self.DFS_words_explored = (
                                        self._do_search("DFS", testing))
        end_time = datetime.now()
        self.DFS_time = end_time - start_time

        #before we do more work, figure out if this was a successful search
        #if not, bail now
        if not self.DFS_path_end:
            if testing:
                print "No path found between", self.start_word, self.end_word
            return False

        #if we get here, we know there is a path, so keep going

        #do BFS, and time it
        start_time = datetime.now()
        self.BFS_path_end, self.BFS_words_explored = (
                                        self._do_search("BFS", testing))
        end_time = datetime.now()
        self.BFS_time = end_time - start_time

        #get each path as a list of words
        self.DFS_path = self._get_path(self.DFS_path_end)
        self.BFS_path = self._get_path(self.BFS_path_end)

        #calculate the efficiency of each search
        #(the + 1 is because we don't examine the end_word but it's counted
        #in the path)
        self.DFS_efficiency = (len(self.DFS_path) /
                               float(self.DFS_words_explored + 1))
        self.BFS_efficiency = (len(self.BFS_path) /
                               float(self.BFS_words_explored + 1))

        #if testing, display the results
        if testing:
            print "\nDFS\n"
            print self.DFS_path
            print "path length:", len(self.DFS_path)
            print self.DFS_time.microseconds / 1000.0, "ms"
            print self.DFS_words_explored, "words explored"
            print "\nBFS\n"
            print self.BFS_path
            print "path length:", len(self.BFS_path)
            print self.BFS_time.microseconds / 1000.0, "ms"
            print self.BFS_words_explored, "words explored"

        #return True to indicated path found
        return True


    def _do_search(self, search_type, testing=False):
        """Perform a DFS or BFS to connect start to end word"""

        #determine the search type and create the corresponding data structure
        #these are all the words waiting to be explored
        if search_type == "DFS":
            to_be_explored = Stack()
        elif search_type == "BFS":
            to_be_explored = Queue()
        else:
            raise Exception("invalid search type")

        #keep track of how many words we explore
        words_explored = 0

        #we'll start with the start_word
        to_be_explored.add(self.start_word)
        used_words = set([self.start_word.word])
        # words_explored += 1

        #as long as there's stuff to examine (and we haven't found the word
        #we're looking for), keep expanding words (figuring out all the legal
        #words we can get to from that word)
        successful_result = None
        while to_be_explored and not successful_result:

            #get the next word to explore/expand
            current_wordnode = to_be_explored.pop_next()

            if testing:
                print "expanding", current_wordnode.word

            #expand that word, grabbing the end of our path if we find it (or
            #rebinding successful_result to None if we don't)
            words_explored += 1
            successful_result = self._find_kids(current_wordnode,
                                                to_be_explored,
                                                used_words)

        #at this point, we've exited the loop, either by running out of words
        #to expand (meaning we never found end_word, and there is no path) or
        #by successfully finding end_word

        #if it's the former, successful_result will still be None
        #if it's the latter, it will be our successful end node
        #return it in either case (also return how many words we expanded)
        return successful_result, words_explored


    def _find_kids(self, current_wordnode, to_be_explored, used_words):
        """Given a word, find all the legal words which are its descendants
           and which haven't already been seen and add them to to_be_explored.
           If we happen to find our goal word, return its WordNode, None
           otherwise.
        """

        #store the word as a list of characters for easy substitution
        current_word_letters = list(current_wordnode.word)

        #considering each character in turn, replace it with every possible
        #letter and, if that makes a legal word, add it to to_be_explored
        #(shuffle to eliminate bias in the order of found words)
        indices = range(self.word_length)
        shuffle(indices)
        for i in indices:
            #shuffle here, too, to eliminate bias
            letters = list("abcdefghijklmnopqrstuvwxyz")
            shuffle(letters)
            for substitute_letter in letters:

                #make a copy of the current word so we can change it
                #without messing up the original
                potential_new_word_letters = current_word_letters[:]

                #substitute in the new letter
                potential_new_word_letters[i] = substitute_letter

                #turn the list of letters back into a string
                potential_new_word = "".join(potential_new_word_letters)

                #if the new word is our goal word, we can stop looking and
                #return it (as a WordNode)
                if potential_new_word == self.end_word.word:
                    return WordNode(potential_new_word, current_wordnode)

                #otherwise, check if that string is a legal word and isn't
                #already in the path
                #note: could do set subtraction here, but that would create
                #a whole new set, and no one needs that
                if (potential_new_word in LEGAL_WORDS and
                    potential_new_word not in used_words):

                    #if it's a new (and real) word, add to the set of
                    #already-used words, then create a WordNode out
                    #of it and add the WordNode to our stack or queue
                    new_word = WordNode(potential_new_word, current_wordnode)
                    to_be_explored.add(new_word)
                    used_words.add(potential_new_word)

        #if we make it all the way through this loop without finding our goal
        #word, we've fully explored all of current_word's potential children
        #and added them to our stack/queue; therefore, fall off the end of the
        #function and return None as a flag indicating that we need to keep
        #searching
        return None
        #(yes, I know this would happen anyway; this is clearer)


    def _get_path(self, path_end):
        """Given the end of the path, return the path as a list of words"""

        #if no path was found, return None
        if not path_end:
            return None

        #add all path nodes, in order, to a list
        path = []

        current = path_end

        while current:
            path.append(current.word)
            current = current.parent

        #the nodes in the path point backwards, so we need to reverse our list
        #to have it display in the right direction
        return path[::-1]


###############################################################################
# Helper functions

def do_searches(start_word, end_word, num_trials):
    """Do the requested number of trials and return a dictionary of the results
    """

    #make sure the search is a legit one - both words have to be legal words,
    #they must be different words, and must be the same length
    errors = []
    if start_word not in LEGAL_WORDS:
        errors.append(start_word + " is not a legal word")
    if end_word not in LEGAL_WORDS:
        errors.append(end_word + " is not a legal word")
    if start_word == end_word:
        errors.append("words must be different")
    if len(start_word) != len(end_word):
        errors.append("words must be of the same length")

    # if errors:



    #make sure there is a path first by running one trial - if not, return None
    test = GameRound(start_word, end_word)
    if not test.play_game():
        return None

    #now that we know there's at least one path between our start and end
    #words, set things up to collect stats and then run the trials

    DFS_times = []
    DFS_path_lengths = []
    DFS_efficiencies = []
    BFS_times = []
    BFS_path_lengths = []
    BFS_efficiencies = []
    sample_trial_num = randint(0, num_trials - 1)

    # run the trials
    for i in xrange(num_trials):

        if i % 10 == 0:
            print i

        #do the search
        trial = GameRound(start_word, end_word)
        trial.play_game()

        #record the results
        DFS_times.append(trial.DFS_time.microseconds / 1000.0)
        DFS_path_lengths.append(len(trial.DFS_path))
        DFS_efficiencies.append(trial.DFS_efficiency)
        BFS_times.append(trial.BFS_time.microseconds / 1000.0)
        BFS_path_lengths.append(len(trial.BFS_path))
        BFS_efficiencies.append(trial.BFS_efficiency)
        if i == sample_trial_num:
            sample_DFS_path = trial.DFS_path
            sample_BFS_path = trial.BFS_path

    #return the data in dictionary form, including everything necessary
    #for adding the data to the database
    return {"DFS": {"search_type": "DFS",
                    "start_word": start_word,
                    "end_word": end_word,
                    "num_letters": len(start_word),
                    "num_trials": num_trials,
                    "avg_path_length": average(DFS_path_lengths),
                    "avg_search_time": average(DFS_times),
                    "avg_efficiency": average(DFS_efficiencies),
                    "med_path_length": median(DFS_path_lengths),
                    "med_search_time": median(DFS_times),
                    "med_efficiency": median(DFS_efficiencies),
                    "sample_path": sample_DFS_path},
            "BFS": {"search_type": "BFS",
                    "start_word": start_word,
                    "end_word": end_word,
                    "num_letters": len(start_word),
                    "num_trials": num_trials,
                    "avg_path_length": average(BFS_path_lengths),
                    "avg_search_time": average(BFS_times),
                    "avg_efficiency": average(BFS_efficiencies),
                    "med_path_length": median(BFS_path_lengths),
                    "med_search_time": median(BFS_times),
                    "med_efficiency": median(BFS_efficiencies),
                    "sample_path": sample_BFS_path}
            }


def average(nums):
    """Return the mean of the given list of values

    >>> average([1, 6, 10, 4, 3])
    4.8

    >>> average([2, 5, 8, 1])
    4.0

    """

    return sum(nums) / float(len(nums))



def median(nums):
    """Return the median value from the given list

    >>> median([3, 5, 1, 4, 2])
    3

    >>> median([3, 2, 4, 1])
    2.5

    """

    sorted_nums = sorted(nums)
    num_count = len(nums)
    if num_count % 2 == 0:
        num1 = sorted_nums[num_count / 2 - 1]
        num2 = sorted_nums[num_count / 2]
        return (num1 + num2) / 2.0
    else:
        return sorted_nums[num_count / 2]


###############################################################################
# Test cases

if __name__ == "__main__":

    from pprint import pprint

    x = GameRound("cat", "dog")
    x.play_game(testing=True)
    x = GameRound("head", "tail")
    x.play_game(testing=True)

    pprint(do_searches("cat", "dog", 100))
