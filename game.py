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


    def __hash__(self):
        """Allow WordNodes to be hashed, for example so they can be added to
           a set without duplication"""

        return hash(self.word)



class GameRound(object):
    """One round of a kids game transforming one word to another"""

    def __init__(self, start_word, end_word):
        self.start_word = WordNode(start_word)
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
        #TODO this shouldn't be brand new each round FIXME
        words_file = open("/usr/share/dict/words")
        legal_words = {line.strip() for line in words_file}

        #do DFS




        #do BFS

    def do_search(self, search_type, legal_words):
        """Perform a DFS or BFS to connect start to end word"""

        #determine the search type and create the corresponding data structure
        if search_type == "DFS":
            to_be_explored = Stack()
        elif search_type == "BFS":
            to_be_explored = Queue()
        else:
            raise Exception("invalid search type")


        #these are all the words waiting to be explored
        #we'll start with the start_word
        to_be_explored.add(self.start_word)

        #this is the current end of the path (technically the head of a linked
        #list which points backwards, so we can get the whole path by starting
        #here and working our way back to the start_word)
        path_tail = self.start_word

        #so that we don't ever have duplicates in the path, store a set of all
        #words used so far (could walk the path linked list to check if we've
        #already included a word, but that's linear and this is constant)
        path_members = set([self.start_word])


        #now, time to do the search

        #as long as there's stuff to examine, examine it and figure out all the
        #places (words) you could get to from each word
        while to_be_explored:

            #store the word as a list of characters for easy substitution
            current_word_letters = list(self.start_word)

            for i in range(self.word_length):
                for substitute_letter in "abcdefghijklmnopqrstuvwxyz":
                    #make a copy of the current word so we can manipulate it
                    potential_new_word_letters = current_word_letters[:]
                    #substitute in the new letter
                    potential_new_word_letters[i] = substitute_letter
                    #turn the list of letters back into a string
                    potential_new_word = "".join(potential_new_word_letters)
                    #check if that string is a legal word
                    #if so, add it to our stack or queue
                    if potential_new_word in legal_words:
                        new_word = potential_new_word
                        to_be_explored.add(new_word)

            #now that we've found all the places we can go from the current word



        #loop over the letters



x = GameRound("cat", "dog")
x.play_game()
