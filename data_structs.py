from collections import deque


class AbstractQuack(object):
    """An abstract class meant to give stacks and queues polymorphism."""

    def __init__(self):
        self.container = self.container_type()


    def __repr__(self):
        """Provide helpful representation when printing."""

        repr_str = "<{cls} length: {length} {first_descriptor}: {first}>"
        return repr_str.format(cls=self.__class__.__name__,
                               length=len(self.container),
                               first_descriptor=self.up_next_descriptor,
                               first=self.peek())


    def __len__(self):
        """Return the current height of the stack or length of the queue."""

        return len(self.container)


    def print_contents(self):
        """Print the contents of the Quack"""

        print self.left_end_descriptor, self.arrow, " ",
        for item in self.container:
            print item,
        print " ", self.arrow, self.right_end_descriptor


    def add(self, item):
        """Add the given item to the container"""

        self.container.append(item)


    def pop_next(self):
        """Remove and return the next item from the container"""

        return self.get_next(self.container)


    def peek(self):
        """Return (but don't remove) the next item to be removed."""

        return self.container[self.peek_index]


    def __nonzero__(self):
        """Define the truthiness/falsiness of the object"""

        return bool(self.container)



class Stack(AbstractQuack):
    """A LIFO data structure"""

    container_type = list
    get_next = staticmethod(list.pop)
    peek_index = -1

    #the following for display purposes only
    up_next_descriptor = right_end_descriptor = "top"
    left_end_descriptor = "bottom"
    arrow = ">"



class Queue(AbstractQuack):
    """A FIFO data structure"""

    container_type = deque
    get_next = staticmethod(deque.popleft)
    peek_index = 0

    #the following for display purposes only
    up_next_descriptor = left_end_descriptor = "front"
    right_end_descriptor = "back"
    arrow = "<"
