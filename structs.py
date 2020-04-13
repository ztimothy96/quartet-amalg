class Node:   
    def __init__(self, data): 
        self.data = data 
        self.next = None
        self.prev = None

class TailedDoublyLinkedList: 
    def __init__(self): 
        self.head = None
        self.tail = None
  
    # Given a reference to the head of a list and an 
    # integer, inserts a new node on the front of list 
    def push(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = self.head
        
        if self.head is not None: 
            self.head.prev = new_node 
        self.head = new_node 
  
    # Given a node as prev_node, insert a new node after 
    # the given node 
    def insertAfter(self, prev_node, new_data): 
        if prev_node is None: 
            print("the given previous node cannot be NULL")
            return 
        new_node = Node(new_data)
        
        if prev_node == self.tail:
            self.tail = new_node
        new_node.next = prev_node.next
        prev_node.next = new_node 
        new_node.prev = prev_node
        
        if new_node.next is not None: 
            new_node.next.prev = new_node 
  
    # Given a reference to the head of DLL and integer, 
    # appends a new node at the end 
    def append(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = None

        if self.head is None: 
            new_node.prev = None
            self.head = new_node
            self.tail = new_node
            return 
  
        self.tail.next = new_node 
        new_node.prev = self.tail
        self.tail = new_node
        return

    # Given node in DLL, delete it and return the next node
    def delete(self, node):
        if node.next == None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
            
        if node.prev == None:
            self.head = node.next
        else:
            node.prev.next = node.next
        return node.next

    # i added this; hope it doesnt screw stuff up
    def delete_specific(self, q):
        curr = self.head
        while(curr is not None):
            temp = curr.next
            if curr.data is q:
                self.delete(curr)
            curr = temp
        
        return


    # Given another DLL, add it to the end of the current DLL
    def union(self, other):
        self.tail.next = other.head
        self.tail = other.tail
  
    # This function prints contents of linked list 
    # starting from the given node 
    def printList(self, node): 
  
        print("\nTraversal in forward direction")
        while(node is not None): 
            print(" % d" %(node.data)), 
            last = node 
            node = node.next
  
        print("\nTraversal in reverse direction")
        while(last is not None): 
            print(" % d" %(last.data)), 
            last = last.prev

    # yeah you read that right; isntEmpty
    # this might be useless
    def isntEmpty(self):
        if self.head == None and self.tail == None:
            return False
        else:
            return True

# This code was modifed from a DoublyLinkedList class contributed by Nikhil Kumar Singh(nickzuck_007) 
