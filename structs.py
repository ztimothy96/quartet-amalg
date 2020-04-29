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
                                        Green Class
(each contains a pointer to candidates, and linked list of green edges)
==========================================================================================
'''

class Green:
    def __init__(self, ptr, lst):
        self.ptr = ptr
        self.lst = lst

    def __str__(self):
        return str(self.ptr) + ", " + str(self.lst)
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

    # Given another DLL, add it to the end of the current DLL
    def union(self, other):
        if (self.tail and not self.head) or (self.head and not self.tail):
            print("something is seriously wrong with this list")
        if self.tail:
            self.tail.next = other.head
        if not self.head:
            self.head = other.head
        self.tail = other.tail
        self.length += other.length
  
    # This function prints contents of linked list 
    def __str__(self):
        node = self.head
        s = "Traversal in forward direction"
        while node:
            s += ", " + str(node.data)
            node = node.next
        return s


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
# assumes that the input tree has distinct labels for each node...
class LCA:
    def __init__(self, root):
        self.height = {} # distance of node from root
        self.first = {} # first index in DFS walk seeing a given node
        self.traversal = [] # the DFS walk through the tree
        self.int2node = [] # maps labels to nodes
        self.dfs(root)
        self.n = len(self.traversal) 
        self.construct_segment_tree()

    def dfs(self, node, height=0):
        self.int2node[node.label] = node
        self.height[node] = height
        self.first[node] = len(self.traversal)
        self.traversal.append(node)
        for child in node.child_node_iter():
            self.dfs(child, height+1)
        self.traversal.append(node)
        return

    # constructs segment tree on heights of the traversal
    def construct_segment_tree(self):
        self.segtree = [(1e9, 0) for _ in range(2*self.n)]
        # leaves
        for i in range(self.n):
            node = self.traversal[i]
            self.segtree[self.n + i] = (self.height[node], node.label)
            
        # remaining nodes  
        for i in range(self.n - 1, 0, -1):  
            self.segtree[i] = min(self.segtree[2*i],  
                             self.segtree[2*i + 1])  
                              
    def range_query(self, left, right): 
        left += self.n  
        right += self.n 
        mi = (1e9, 0) # initialize minimum to a very high value
        
        while (left < right): 
            if (left & 1): # check if odd
                    mi = min(mi, self.segtree[left]) 
                    left = left + 1
            if (right & 1): 
                    right -= 1
                    mi = min(mi, self.segtree[right]) 

            # move to the next higher level
            left = left // 2
            right = right // 2
        
        return self.int2node[mi[1]]

    # find lca of nodes i,j
    def query(self, i, j):
        left = self.first[i]
        right = self.first[j]
        if left > right:
            left, right = right, left
        return self.range_query(left, right)
        
