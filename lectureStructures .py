class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    # MODIFY: RAISE AN EXCEPTION IF THIS METHOD IS INVOKED ON AN EMPTY STACK
    def pop(self):
        if self.isEmpty():
            raise Exception('stack is empty')
        return self.items.pop()

    # MODIFY: RAISE AN EXCEPTION IF THIS METHOD IS INVOKED ON AN EMPTY STACK
    def peek(self):
        if self.isEmpty():
            raise Exception
        return self.items[len(self.items) - 1]

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def show(self):
        print(self.items)

    def __str__(self):
        stackAsString = '['
        for item in self.items:
            stackAsString += str(item)
        return stackAsString+']'

    def clear(self):
        if not self.isEmpty():
            self.items.clear()
        # TO DO: complete method according to updated ADT


class BoundedQueue:
    # Creates a new empty queue:
    def __init__(self, capacity):
        assert isinstance(capacity, int), (
                    'Error: Type error: %s' % (type(capacity)))  # throws an assertion error on not true
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.items = []  # init the  list / queue as empty
        self.__capacity = capacity

    # Adds a new item to the back of the queue, and returns nothing:
    def enqueue(self, item):
        '''
        Enqueue the element to the back of the queue
        :param item: the element to be enqueued
        :return: No returns
        '''

        if len(self.items) >= self.__capacity:
            raise Exception('Error: Queue is full')
        self.items.append(item)
        ##### START CODE HERE #####
        '''
        Remember to check the conditions
        '''
        #####  END CODE HERE ######

    # Removes and returns the front-most item in the queue.
    # Returns nothing if the queue is empty.
    def dequeue(self):
        '''
        Dequeue the element from the front of the queue and return it
        :return: The object that was dequeued
        '''

        ##### START CODE HERE #####
        '''
        1. remember to check the conditions
        2. return the appropriate value
        '''
        if len(self.items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.items.pop(0)

        #####  END CODE HERE ######

    # Returns the front-most item in the queue, and DOES NOT change the queue.
    def peek(self):
        if len(self.items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.items[0]

    # Returns True if the queue is empty, and False otherwise:
    def is_empty(self):
        return len(self.items) == 0

    # Returns True if the queue is full, and False otherwise:
    def is_full(self):
        return len(self.items) == self.__capacity

    # Returns the number of items in the queue:
    def size(self):
        return len(self.items)

    # Returns the capacity of the queue:
    def capacity(self):
        return self.__capacity

    # Removes all items from the queue, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.items = []

    # Returns a string representation of the queue:
    def __str__(self):
        str_exp = ""
        for item in self.items:
            str_exp += (str(item) + " ")
        return str_exp

    # Returns a string representation of the object bounded queue:
    def __repr__(self):
        return str(self) + " Max=" + str(self.__capacity)


class CircularQueue:
    # Creates a new empty queue:
    def __init__(self, capacity):
        # Check validity of capacity type and value
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity)))
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))

        # Initialize private attributes
        self.items = []
        self.__capacity = capacity
        self.count = 0
        self.head = 0
        self.tail = 0

        # Allocate space for the circular queue
        for i in range(self.__capacity):
            self.items.append(None)

    # Adds a new item to the back of the queue, and returns nothing:
    def enqueue(self, item):
        '''
        This function enqueues the item into the back of the queue
        :param item: The  item to  be queued
        :return: No returns
        '''

        ##### START CODE HERE #####
        '''
        Remember to check the proper conditions 
        '''
        if self.count == self.__capacity:
            raise Exception('Error: Queue is full')
        if len(self.items) < self.__capacity:
            self.items.append(item)
        else:
            self.items[self.tail] = item
        self.count += 1
        self.tail = (self.tail + 1) % self.__capacity
        #####  END CODE HERE ######

    # Removes and returns the front-most item in the queue.
    # Returns nothing if the queue is empty.
    def dequeue(self):
        '''
        Dequeue the the element from the front of the queue and return the value
        :return: Returns the object that is dequeued
        '''

        ##### START CODE HERE #####
        '''
        Remember to check the proper conditions (some hints)
        1. get item at the head of queue
        2. remove the item from the head of queue
        3. decrease stored size of queue
        4. Shift the head
        5. return the item
        '''
        if self.count == 0:
            raise Exception('Error: Queue is empty')
        item = self.items[self.head]
        self.items[self.head] = None
        self.count -= 1
        self.head = (self.head + 1) % self.__capacity
        return item
        #####  END CODE HERE ######

    # Returns the front-most item in the queue, and DOES NOT change the queue.
    def peek(self):
        if self.count == 0:
            raise Exception('Error: Queue is empty')

        return self.items[self.head]

    # Returns True if the queue is empty, and False otherwise:
    def is_empty(self):
        return self.count == 0

    # Returns True if the queue is full, and False otherwise:

    # Returns the number of items in the queue:
    def size(self):
        return self.count

    # Returns the capacity of the queue:
    def capacity(self):
        return self.__capacity

    # Removes all items from the queue, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.items = []
        self.count = 0
        self.head = 0
        self.tail = 0

    # Returns a string representation of the queue:
    def __str__(self):
        str_exp = "["
        i = self.head
        for j in range(self.count):
            str_exp += str(self.items[i]) + " "
            i = (i + 1) % self.__capacity
        return str_exp + "]"

    # Returns a string representation of the object CircularQueue
    def __repr__(self):
        return str(self) + " H= " + str(self.head) + " T=" + str(self.tail) + " (" + str(self.count) + "/" + str(self.__capacity) + ")"

    def is_full(self):
        print(self.tail)
        print(self.head)
        return self.head == (self.tail+1) % self.__capacity