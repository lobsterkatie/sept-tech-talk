from data_structs import Stack, Queue


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
        return repr_str.format(word=self.word, arent=self.parent)


    def __eq__(self, other):
        """Allow WordNodes to be compared using =="""

        return self.word == other.word


    def __ne__(self, other):
        """Allow WordNodes to be compared using !="""

        return not self.__eq__(other)


    #FIXME not sure this is needed anymore, if the set (which I may not even
    #use now) is only of the strings, rather than of the whole nodes
    #of course, that latter change not only makes the code a little cleaner, it
    #actually makes more sense, because two word nodes might have the same
    #word value but have different parents, so they're fundamentally not the
    #same
    def __hash__(self):
        """Allow WordNodes to be hashed, for example so they can be added to
           a set without duplication"""

        return hash(self.word)



class GameRound(object):
    """One round of a kids game transforming one word to another"""

    def __init__(self, start_word, end_word):
        self.start_word = WordNode(start_word)
        #TODO decide if it's worth it to wrap end_word in a WordNode, and make
        #a comment about why we're doing so (ability to compare to current_word)
        #if it does get left this way
        self.end_word = WordNode(end_word)
        # self.DFS_path = [start_word]
        # self.BFS_path = [start_word]
        self.DFS_path_tail = self.start_word
        self.BFS_path_tail = self.start_word
        self.word_length = len(start_word)
        self.path_found = False

    def play_game(self):
        """Play the game, recording DFS and BFS solution paths"""

        #get set of legal words
        #FIXME this shouldn't be brand new each round
        words_file = open("/usr/share/dict/words")
        legal_words = {line.strip() for line in words_file}

        #do DFS




        #do BFS

    def do_search(self, search_type, legal_words):
        """Perform a DFS or BFS to connect start to end word"""

        #determine the search type and create the corresponding data structure
        #these are all the words waiting to be explored
        if search_type == "DFS":
            to_be_explored = Stack()
        elif search_type == "BFS":
            to_be_explored = Queue()
        else:
            raise Exception("invalid search type")


        # #we'll start with the start_word
        # to_be_explored.add(self.start_word)

        #this is the current end of the path (technically the head of a linked
        #list which points backwards, so we can get the whole path by starting
        #here and working our way back to the start_word)
        path_tail = None

        #so that we don't ever have duplicates in the path, store a set of all
        #words used so far (not WordNodes, just the words themselves; we could
        #walk the path to check if we've already included a word, but that's
        #linear (the path is a linked list) and this is constant)
        path_members = set()


        #now, time to do the search

        #as long as there's stuff to examine, examine it and figure out all the
        #places (words) you could get to from each word
        while to_be_explored:

            #get the current word
            current_word = to_be_explored.pop_next()

            #put it in the path by including the word in our set and moving the
            #tail pointer
            #(since each WordNode is created knowing who its parent is, as long
            #as we have the last word in the path, we have the whole path)
            path_members.add(current_word.word)
            path_tail = current_word

            #check if we've reached our destination, that is, if current_word
            #is end_word; if so, stop looking
            if current_word == self.end_word:
                break

            #if we get to here, we know that current_word != end_word, so
            #"explore" it, that is, figure out all the places we can go from
            #it and add them to to_be_explored

            #store the word as a list of characters for easy substitution
            current_word_letters = list(current_word)

            #considering each character in turn, replace it with every possible
            #letter and, if that makes a legal word, add it to
            #to_be_explored
            for i in range(self.word_length):
                for substitute_letter in "abcdefghijklmnopqrstuvwxyz":

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
                    if (potential_new_word in legal_words and
                        potential_new_word not in path_members):

                        #if it's a new (and real) word, create a WordNode out
                        #of it and add it to our stack or queue
                        new_word = WordNode(potential_new_word, current_word)
                        to_be_explored.add(new_word)

            #now that we've found all the places we can go from the current
            #word, move on to the next word

            #depending on what kind of search we're doing (DFS vs BFS), whether
            #or not current_word is a leaf (it has no legal kids which aren't
            #already in its path), where current_word is in the "birth order,"
            #etc, etc, the next word may or may not have current_word as a
            #parent

            #if current_word is the next word's parent, we want to keep
            #current_word in the set of all words in our path

            #if not, we're effectively backtracking, meaning we want to take it
            #out




            #if we're doing DFS, the next word will be one of current_word's
            #children, if any

            #if current_word is a leaf (it has no legal kids which aren't
            #already in its path) or if we're doing BFS, the next word will
            #either be a sibling or non-direct ancestor (aunt/uncle, grand aunt/
            #grand uncle, etc)



        #loop over the letters



x = GameRound("cat", "dog")
x.play_game()
