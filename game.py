from data_structs import Stack, Queue
from random import shuffle
from datetime import datetime


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



class GameRound(object):
    """One round of a kids game transforming one word to another"""

    def __new__(cls, start_word, end_word):
        """Only create the GameRound if words are the same length"""

        if len(start_word) != len(end_word):
            raise Exception("words must be the same length")
        else:
            return super(GameRound, cls).__new__(cls, start_word, end_word)


    def __init__(self, start_word, end_word):
        self.start_word = WordNode(start_word)
        self.end_word = WordNode(end_word)
        self.word_length = len(start_word)

    def play_game(self):
        """Play the game, recording DFS and BFS solution paths"""


        #do DFS, and time it
        start_time = datetime.now()
        self.DFS_path = self._do_search("DFS")
        end_time = datetime.now()
        self.DFS_time = end_time - start_time

        #do BFS, and time it
        start_time = datetime.now()
        self.BFS_path = self._do_search("BFS")
        end_time = datetime.now()
        self.BFS_time = end_time - start_time

        #display the results
        print "\nDFS\n"
        self._print_path(self.DFS_path)
        print self.DFS_time.microseconds / 1000.0, "ms"
        print "\nBFS\n"
        self._print_path(self.BFS_path)
        print self.BFS_time.microseconds / 1000.0, "ms"



    def _do_search(self, search_type):
        """Perform a DFS or BFS to connect start to end word"""

        #determine the search type and create the corresponding data structure
        #these are all the words waiting to be explored
        if search_type == "DFS":
            to_be_explored = Stack()
        elif search_type == "BFS":
            to_be_explored = Queue()
        else:
            raise Exception("invalid search type")

        #we'll start with the start_word
        to_be_explored.add(self.start_word)
        used_words = set([self.start_word.word])

        #as long as there's stuff to examine, examine it and figure out all the
        #places (words) you could get to from each word
        while to_be_explored:

            #get the current word
            current_word = to_be_explored.pop_next()

            #check if we've reached our destination, that is, if current_word
            #is end_word; if so, stop looking
            if current_word == self.end_word:
                break

            #if we get to here, we know that current_word != end_word, so
            #"explore" it, that is, figure out all the places we can go from
            #it and add them to to_be_explored

            #store the word as a list of characters for easy substitution
            current_word_letters = list(current_word.word)

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

                    #check if that string is a legal word and isn't already
                    #in the path
                    #note: could do set subtraction here, but that would create
                    #a whole new set, and no one needs that
                    if (potential_new_word in LEGAL_WORDS and
                        potential_new_word not in used_words):

                        #if it's a new (and real) word, add to the set of
                        #already-used words, then create a WordNode out
                        #of it and add the WordNode to our stack or queue
                        new_word = WordNode(potential_new_word, current_word)
                        to_be_explored.add(new_word)
                        used_words.add(potential_new_word)

            #now that we've found all the places we can go from the current
            #word, move on to the next word

        #once we get here, we've either found our end_word or run out of places
        #to look - return the appropriate thing in either case
        if current_word == self.end_word:

            #we found a valid path - return the last word, which is the head
            #of a linked list contianing the path
            return current_word

        else:

            #there was no valid path, and we've run out of words to check, so
            #return None as a flag to denote that
            return None



    def _print_path(self, path_end):
        """Print the path"""

        if not path_end:
            print "No path found"
            return

        #FIXME make this print out more nicely

        #add all path nodes, in order, to a list
        path = []

        current = path_end

        while current:
            path.append(current.word)
            current = current.parent

        #the nodes in the path point backwards, so we need to reverse our list
        #to have it display in the right direction
        print path[::-1]






#get set of legal words
with open("/usr/share/dict/words") as words_file:
    LEGAL_WORDS = {line.strip() for line in words_file}


x = GameRound("cat", "dog")
x.play_game()
x = GameRound("circle", "square")
x.play_game()

