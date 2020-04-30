import dendropy
import structs
from bisect import bisect_right

# convert all taxa to integers 0 through n-1
# quartets represented in Newick notation ((a, b), (c, d))
'''
==========================================================================================
                                        WATC Class
==========================================================================================
'''
class WATC:
    def __init__(self, n, quartets):
        self.n = n
        self.quartets = sorted(quartets)
        self.make_colorful_things()
        self.make_edis()
        self.tree = [i for i in range(self.n)]
        self.make_candidates() #doubly linked list
        return


    # wrapper function to run WATC algorithm
    def get_tree(self):
        T = self.find_some_tree()
        if self.verify_tree(T):
            return T
        return "Fail"
    '''
    ------------------------------------------------------------------------------------------
                                          Wrapper functions
                                (functions for Stage 1 and Stage 2)
    ------------------------------------------------------------------------------------------
    '''
    # Stage 1 wrapper
    def find_some_tree(self):
        m = len(self.edis)
        while m >= 4:
            
            #brute force the base case
            if m == 4:                        
                reps = list(self.edis.keys())
                all_edges = [(i, j) for j in range(4) for i in range(j) if self.are_siblings(reps[i], reps[j])]
                
                if all_edges == [(0, 1), (2, 3)]:
                    x, y, z, w = reps[0], reps[1], reps[2], reps[3]
                elif all_edges == [(0, 2), (1, 3)]:
                    x, y, z, w = reps[0], reps[2], reps[1], reps[3]
                elif all_edges == [(1, 2), (0, 3)]:
                    x, y, z, w = reps[1], reps[2], reps[0], reps[3]
                else:
                    print("Fail: bad base case")
                    return "Fail"
                
                t1 = self.merge_edi_trees(x, y)
                t2 = self.merge_edi_trees(z, w)
                T = dendropy.Tree()
                T.seed_node.add_child(t1.seed_node)
                T.seed_node.add_child(t2.seed_node)
                return T
            
            else:                            
                sibs = self.find_siblings()
                if sibs:
                    i, j = sibs
                    self.update_structures(i, j)
                    m = len(self.edis)
                    print("There are " + str(m) + " edi-trees left.")
                else:
                    print("Fail: no more candidates")
                    return "Fail"
                
        return "Fail"
    
    # Stage 2 Wrapper
    def verify_tree(self, T):
        rep_quartets = self.get_rep_quartets(T)
        return self.are_reps_in_quartets(rep_quartets) and self.are_quartets_in_tree(T)           

    '''
    ------------------------------------------------------------------------------------------
                                          Constructors
                                (functions to initialize all data structures)
    ------------------------------------------------------------------------------------------
    '''
    def make_colorful_things(self):
        self.red = [[0 for j in range(self.n)] for i in range(self.n)]
        self.green = [[structs.Green(None, structs.TailedDoublyLinkedList()) for j in range(self.n)] for i in range(self.n)]
        for q in self.quartets:
            gedges = self.green_edges(q)
            redges = self.red_edges(q)
            
            # update number of red egdes
            for (x,y) in redges:
                self.red[x][y] += 1
                self.red[y][x] += 1

            #update set of green edges
            for (u,v) in gedges:
                self.green[u][v].lst.append(q)
                self.green[v][u].lst.append(q)
        return

    def make_edis(self):
        self.edis = {}
        for i in range(self.n):
            tree = dendropy.Tree()
            leaf = tree.seed_node
            leaf.label = str(i)
            self.edis[i] = tree
        return

    def make_candidates(self):
        self.candidates = structs.TailedDoublyLinkedList()
        for i in range(self.n):
            for j in range(i):
                lst1 = self.green[i][j].lst
                # check if edge is a candidate
                if not lst1.isEmpty():
                    self.candidates.append((i,j))
                    self.green[i][j].ptr = self.candidates.tail
                    self.green[j][i].ptr = self.candidates.tail
        return 

    def green_edges(self, q):
        ((i, j), (k, l)) = q
        return [(i, j), (k, l)]

    def red_edges(self, q):
        ((i, j), (k, l)) = q
        return [(i, k), (i,l), (j, k), (j, l)]
    
    '''
    ------------------------------------------------------------------------------------------
                                          Stage 1 Helpers
                                (functions to help find a tree)
    ------------------------------------------------------------------------------------------
    '''

    def are_siblings(self, i, j):
        if self.red[i][j] != 0 or self.tree[i] != i or self.tree[j] != j:
            return False
        return self.has_green_edge(i, j)
        
    # returns a valid sibling pair from candidates to merge edi-trees
    def find_siblings(self):
        curr = self.candidates.head
        while(curr is not None):
            (i, j) = curr.data
            if self.tree[i] != i or self.tree[j] != j:
                curr = self.candidates.delete(curr)
            elif self.red[i][j] != 0:
                curr = curr.next
            elif self.has_green_edge(i, j):
                return (i, j)
            else:
                curr = self.candidates.delete(curr)
        return None

    # returns whether there is a non-ghost green edge between i, j
    # also deletes ghost edges in checking process
    def has_green_edge(self, i, j):
        lst = self.green[i][j].lst
        node = lst.head
        while node != None:
            q = node.data
            if self.is_ghost_edge(i, j, q):
                node = lst.delete(node)
            else:
                return True
            
        # empty list; disconnect ptrs in green
        self.green[i][j].ptr = None
        self.green[j][i].ptr = None
        return False

    # returns whether (a, b) is a ghost edge for quartet q
    def is_ghost_edge(self, a, b, q):
        ((x, y), (z, w)) = q
        nodes = [x, y, z, w]
        [c, d] = [t for t in nodes if t != a and t != b]
        return self.tree[c] == self.tree[d]

    def update_structures(self, i, j):
        # first delete the red edges associated to edge (i, j)
        curr = self.green[i][j].lst.head
        while (curr is not None):
            ((a, b), (c, d)) = curr.data
            q = ((self.tree[a], self.tree[b]), (self.tree[c], self.tree[d]))
            redges = self.red_edges(q)
            for (x,y) in redges:
                self.red[x][y] -= 1
                self.red[y][x] -= 1
            curr = curr.next
                
        i, j = sorted([i, j])
        self.merge_edi_trees(i, j)
        self.update_tree(i, j)
        self.update_colors(i, j)
        pass
    
    # merges two edi-trees at a root; labeled by lesser index
    def merge_edi_trees(self, i, j):
        if i==j:
            raise ValueError('cannot merge with self')
        i, j = sorted([i, j])
        parent = dendropy.Tree()
        parent.seed_node.add_child(self.edis[i].seed_node)
        parent.seed_node.add_child(self.edis[j].seed_node)
        self.edis[i] = parent
        del self.edis[j]
        return parent

    '''
     **** things we may need to debug (not clear yet) ****
     - for update_tree & update_colors, we go through all k != i, 
       but paper says k should be every other edi-tree (maybe it doesnt
       matter, but maybe its more efficient to iterate through the trees array)
    '''

    def update_tree(self, i, j):
        for k in range(self.n):
            if self.tree[k] == j:
                self.tree[k] = i
        return

    def update_colors(self, i, j):
        for k in list(self.edis.keys()):
            if k != i and k != j:
                # update red
                redBefore = self.red[i][k]
                self.red[i][k] = self.red[i][k] + self.red[j][k]
                self.red[k][i] = self.red[k][i] + self.red[k][j]

                # deleting candidates 
                if redBefore == 0 and self.red[i][k] > 0: 
                    delCand = self.green[i][k].ptr
                    self.candidates.delete(delCand)
                    self.green[i][k].ptr = None
                    self.green[k][i].ptr = None
                
                # update green
                greenBefore = self.green[i][k].lst.length
                self.green[i][k].lst.union(self.green[j][k].lst)
                self.green[k][i].lst.union(self.green[k][j].lst)
                
                # inserting candidates 
                if greenBefore == 0 and self.green[i][k].lst.length > 0:
                    self.candidates.append((i,k))
                    self.green[i][k].ptr = self.candidates.tail
                    self.green[k][i].ptr = self.candidates.tail

                # lets do this for safety
                self.red[j][k] = -float('inf')
                self.red[k][j] = -float('inf')
                self.green[j][k] = None
                self.green[k][j] = None

        # just for clarity
        self.red[i][j] = -float('inf')
        self.red[j][i] = -float('inf')
        self.red[j][j] = -float('inf')
        self.green[i][j] = None
        self.green[j][i] = None
        return
                
    '''
    ------------------------------------------------------------------------------------------
                                          Stage 2 Helpers
                                (functions to help verify the tree)
    ------------------------------------------------------------------------------------------
    '''
    # returns distance and label of minimal closest leaf
    def get_rep(self, root):
        if root.is_leaf():
            return 0, int(root.label)
        child_reps = sorted([self.get_rep(child) for child in root.child_node_iter()])
        dist, label = child_reps[0]
        return dist+1, label

    # returns the child of node which is not the given one
    def get_other_child(self, node, child):
        others = [other for other in node.child_node_iter() if other != child]
        if len(others) != 1:
            raise ValueError('wrong child, or not an internal node of a binary tree')
        return others[0]

    # returns the representative of the short quartets in the input tree
    def get_rep_quartets(self, T):
        reps = {}
        rep_quartets = []
        # gets representative for each node
        for node in T.preorder_node_iter():
            reps[node] = self.get_rep(node)[1]
        
        # constructs short quartet for each edge
        for edge in T.preorder_internal_edge_iter(exclude_seed_edge=True):
            head = edge.head_node
            tail = edge.tail_node
            # get children of head
            i, j = [reps[child] for child in head.child_node_iter()]
            # if tail has no parent, then the other part of the quartet is 
            # the reps of children of head's sibling
            # else, get one of head's siblings and tail's siblings
            if tail == T.seed_node:
                tail = self.get_other_child(tail, head)
                k, l= [reps[child] for child in tail.child_node_iter()]
            else:
                k = reps[self.get_other_child(tail, head)]
                parent = tail.parent_node
                l = reps[self.get_other_child(parent, tail)]
            top = ((i, j), (k, l))
            rep_quartets.append(top)
        
        return rep_quartets

    # returns whether input quartet q is inside quartet list via binary search
    def in_quartets(self, q):
        # confused as to whether this works..
        i = bisect_right(self.quartets, q)
        return i != len(self.quartets)+1 and self.quartets[i-1] == q

    # returns list of quartets which induce same split as q
    def same_splits(self, q):
        ((i, j), (k, l)) = q
        return [((i, j), (k, l)), ((j, i), (k, l)), ((i, j), (l, k)), ((j, i),(l, k)),
                ((k, l), (i, j)), ((k, l), (j, i)), ((l, k), (i, j)), ((l, k), (j, i))]

    # returns whether computed representative quartets are contained in input quartets
    def are_reps_in_quartets(self, rep_quartets):
        return all(any(self.in_quartets(q) for q in self.same_splits(rep)) for rep in rep_quartets)

    # returns whether the input quartets are induced by tree T
    def are_quartets_in_tree(self, T):
        lca = structs.LCA(T.seed_node, self.n)
        for q in self.quartets:
            ((i, j), (k, l)) = q
            lj, lk, ll = lca.query(i, j), lca.query(i, k), lca.query(i, l)
            if lj == lk:
                top = ((i, l), (j, k))
            elif lj == ll:
                top = ((i, k), (j, l))
            elif lk == ll:
                top = ((i, j), (k, l))
            else:
                raise ValueError('invalid tree topology')
            if top not in self.same_splits(q):
                return False
        return True
