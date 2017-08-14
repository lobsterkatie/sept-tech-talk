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

        # pop_method = list.pop

        # pop_method = self.get_next
        # return pop_method(self.container)

        return self.get_next(self.container)



        # return self.container.method()

        # return getattr(self, get_next)()

        #WORKS
        # return eval("self.container." + self.get_next + "()")



    def peek(self):
        """Return (but don't remove) the next item to be removed."""

        return self.container[self.peek_index]


    def __nonzero__(self):
        """Define the truthiness/falsiness of the object"""

        return bool(self.container)




class Stack(AbstractQuack):
    """A LIFO data structure"""

    container_type = list
    # get_next = "pop"
    get_next = staticmethod(list.pop)
    peek_index = -1

    #the following for display purposes only
    up_next_descriptor = right_end_descriptor = "top"
    left_end_descriptor = "bottom"
    arrow = ">"


    # def __init__(self):
    #     self._stack = []

    # def __repr__(self):
    #     """Provide helpful representation when printing."""

    #     repr_str = "<Stack length: {length} top: {top}>"
    #     return repr_str.format(length=len(self._stack),
    #                            top=self.peek())

    # def __len__(self):
    #     """Return the current height of the stack."""

    #     return len(self._stack)

    # def print_stack(self):
    #     """Print the contents of the stack."""

    #     print "bottom > ",
    #     for item in self._stack:
    #         print item,
    #     print " > top"

    # def push(self, item):
    #     """Add the given item to the top of the stack."""

    #     self._stack.append(item)

    # def pop(self):
    #     """Remove and return the top item on the stack."""

    #     return self._stack.pop()

    # def peek(self):
    #     """Return (but don't remove) the top item on the stack."""

    #     return self._stack[-1]



class Queue(AbstractQuack):
    """A FIFO data structure"""

    container_type = deque
    get_next = staticmethod(deque.popleft)
    # get_next = "popleft"
    peek_index = 0

    #the following for display purposes only
    up_next_descriptor = left_end_descriptor = "front"
    right_end_descriptor = "back"
    arrow = "<"

    # def __init__(self):
    #     self._queue = deque()

    # def __repr__(self):
    #     """Provide helpful representation when printing.

    #     >>> q = Queue()
    #     >>> q._queue = deque([1, 2, 3])
    #     >>> q
    #     <Queue length: 3 front: 1>

    #     """

    #     repr_str = "<Queue length: {length} front: {front}>"
    #     return repr_str.format(length=len(self._queue),
    #                            front=self.peek())

    # def __len__(self):
    #     """Return the current length of the queue."""

    #     return len(self._queue)

    # def print_queue(self):
    #     """Print the contents of the queue."""

    #     print "front > ",
    #     for item in self._queue:
    #         print item,
    #     print " > back"

    # def enqueue(self, item):
    #     """Add the given item to the end of the queue."""

    #     self._queue.append(item)

    # def dequeue(self):
    #     """Remove and return the first item in the queue."""

    #     return self._queue.popleft()

    # def peek(self):
    #     """Return (but don't remove) the first item in the queue."""

    #     return self._queue[0]




