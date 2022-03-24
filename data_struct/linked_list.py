class Node: 
    def __init__(self, value, previous) -> None:
        self.value = value
        self.previous = previous
        self.next = None

class LinkedList: 
    def __init__(self) -> None:
        self.firths = None
        self.last = None

    @property
    def empty(self):
        return self.last is None or self.firths is None

    def append(self, value):
        node = Node(value, self.firths)
        if self.firths is None: self.firths = node
        else: self.firths.next = node

        self.last = node

class LinkedListLIFO(LinkedList):
    def pop(self):
        value = self.last.value
        self.last = self.last.previous
        return value


class LinkedListFIFO(LinkedList):
    def pop(self):
        value = self.firths.value
        self.firths = self.firths.previous
        return value