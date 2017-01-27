class Queue:
    """
    Queue implementation
    """
    def __init__(self):
        self.queue = []
    def isEmpty(self):
        return len(self.queue) == 0
    def enqueue(self, e):
        self.queue.append(e)
    def dequeue(self):
        return self.queue.pop(0)
    def __len__(self):
        return len(self.queue)

class Stack:
    """
    Stack implementation
    """
    def __init__(self):
        self.stack = []
    def isEmpty(self):
        return len(self.stack) == 0
    def push(self, e):
        self.stack.insert(0, e)
    def pop(self):
        return self.stack.pop(0)
    def __len__(self):
        return len(self.stack)

if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(3)
    s.push(0)
    print s.stack
    print s.pop()
    print s.pop()
    print s.stack
    print s.pop()
