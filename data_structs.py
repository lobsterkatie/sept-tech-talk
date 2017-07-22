from collections import deque

class Stack(object):
    """A LIFO data structure"""

    def __init__(self):
        self._stack = []

    def __repr__(self):
        """Provide helpful representation when printing."""

        repr_str = "<Stack length: {length} top: {top}>"
        return repr_str.format(length=len(self._stack),
                               top=self.peek())

    def __len__(self):
        """Return the current height of the stack."""

        return len(self._stack)

    def print_stack(self):
        """Print the contents of the stack."""

        print "bottom > ",
        for item in self._stack:
            print item,
        print " > top"

    def push(self, item):
        """Add the given item to the top of the stack."""

        self._stack.append(item)

    def pop(self):
        """Remove and return the top item on the stack."""

        return self._stack.pop()

    def peek(self):
        """Return (but don't remove) the top item on the stack."""

        return self._stack[-1]



class Queue(object):
    """A FIFO data structure"""

    def __init__(self):
        self._queue = deque()

    def __repr__(self):
        """Provide helpful representation when printing."""

        repr_str = "<Queue length: {length} front: {front}>"
        return repr_str.format(length=len(self._queue),
                               front=self.peek())

    def __len__(self):
        """Return the current length of the queue."""

        return len(self._queue)

    def print_queue(self):
        """Print the contents of the queue."""

        print "front > ",
        for item in self._queue:
            print item,
        print " > back"

    def enqueue(self, item):
        """Add the given item to the end of the queue."""

        self._queue.append(item)

    def dequeue(self):
        """Remove and return the first item in the queue."""

        return self._queue.popleft()

    def peek(self):
        """Return (but don't remove) the first item in the queue."""

        return self._queue[0]




