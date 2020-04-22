'''
==========================================================================================
                                        Node Class
                                    (to use for Tailed DLL)
==========================================================================================
'''

class Node:   
    def __init__(self, data): 
        self.data = data 
        self.next = None
        self.prev = None


'''
==========================================================================================
                                        Tailed DLL
(The DoublyLinkedList class was modified from code by Nikhil Kumar Singh (nickzuck_007))
==========================================================================================
'''
class TailedDoublyLinkedList: 
    def __init__(self): 
        self.head = None
        self.tail = None
        self.length = 0 
        # added length attribute; hopefully it is updated correctly in functions
  
    # Given a reference to the head of a list and an 
    # integer, inserts a new node on the front of list 
    def push(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = self.head
        
        if self.head is not None: 
            self.head.prev = new_node 
        self.head = new_node 
        self.length += 1
  
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
        self.length += 1
  
    # Given a reference to the head of DLL and integer, 
    # appends a new node at the end 
    def append(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = None
        self.length += 1
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
        self.length -= 1
        return node.next

    # i added this; hope it doesnt screw stuff up
    def delete_specific(self, q):
        curr = self.head
        while(curr is not None):
            temp = curr.next
            if curr.data is q:
                self.delete(curr)
            curr = temp
        self.length -= 1
        return


    # Given another DLL, add it to the end of the current DLL
    def union(self, other):
        self.tail.next = other.head
        self.tail = other.tail
        self.length += other.length
  
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
        return self.length > 0

    def isEmpty(self):
        return self.length == 0



'''
==========================================================================================
                                        LCA Class
                (The segment tree was modified from code by Sarthak Raghuwanshi) 
==========================================================================================
'''

# a data structure for finding least common ancestor in O(log n) time
class LCA:
    def __init__(self, root):
        self.height = {} # distance of node from root
        self.first = {} # first index in DFS walk seeing a given node
        self.traversal = [] # the DFS walk through the tree
        self.node2int = {} # labels for each node
        self.int2node = []
        self.dfs(root)
        self.n = len(self.node2int) # size of input tree
        self.construct_segment_tree()

    def dfs(self, node, height=0):
        self.node2int[node] = len(self.node2int)
        self.int2node.append(node)
        self.height[node] = height
        self.first[node] = len(traversal)
        for child in node.child_node_iter():
            self.dfs(child, height+1)
            self.traversal.append(child)
        return

    # constructs segment tree
    # a is array of values
    def construct_segment_tree(self):
        self.segtree = [0 for _ in range(2*self.n)]
        # leaves
        for i in range(self.n):  
            self.segtree[self.n + i] = self.height[i]
          
        # remaining nodes  
        for i in range(self.n - 1, 0, -1):  
            self.segtree[i] = min(self.segtree[2 * i],  
                             self.segtree[2 * i + 1])  
                              
    def range_query(self, left, right): 
        left += self.n  
        right += self.n 
          
        """ Basically the left and right indices  
            will move towards right and left respectively  
            and with every each next higher level and  
            compute the minimum at each height change  
            the index to leaf node first """
        mi = 1e9 # initialize minimum to a very high value 
        while (left < right): 
            if (left & 1): # if left index in odd  
                    mi = min(mi, segtree[left]) 
                    left = left + 1
            if (right & 1): # if right index in odd  
                    right -= 1
                    mi = min(mi, segtree[right]) 
                      
            # move to the next higher level 
            left = left // 2
            right = right // 2
        return mi 

    # find lca of nodes i,j
    def query(self, i, j):
        left = self.first[i]
        right = self.first[j]
        if left > right:
            left, right = right, left
        return self.range_query(left, right)
        
