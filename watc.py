import dendropy
import networkx as nx
import structs
from bisect import bisect_right

# convert all taxa to integers 0 through n-1
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
        self.tree = range(n)
        self.make_candidates() #doubly linked list
        self.names = dendropy.TaxonNamespace([str(i) for i in range(self.n)])
        return


    # wrapper function to run WATC algorithm
    def get_tree(self):
        T = self.find_some_tree()
        if self.verify_tree(T):
            return T
        else:
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
                x = self.edis.keys()[0]
                
                if len(self.graph.neighbors(x)) != 1:
                    return "Fail"
                y = self.graph.neighbors(x)[0]
                
                if len(self.graph.neighbors(y)) != 1:
                    return "Fail"
                
                self.graph.remove_nodes_from([x, y])
                z = self.edis.keys()[0]
                
                if len(self.graph.neighbors(z)) != 1:
                    return "Fail"
                
                w = self.graph.neighbors(z)[0]
                t1 = merge_edi_trees(x, y)
                t2 = merge_edi_trees(z, w)
                T = merge_edi_trees(t1, t2)
                return T
            
            else:
                sibs = self.find_siblings()
                if sibs:
                    i, j = sibs
                    self.update_structures(i, j)
                    # i feel like we should update m in order for this while loop to eventually end..
                    m = len(self.edis)
                    print("There are " + str(m) + " trees left.")
                else:
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
        self.graph = nx.Multigraph()
        self.graph.add_nodes_from(range(0, self.n))
        self.red = [[0 for j in range(self.n)] for i in range(self.n)]
        self.green = [[(None, structs.TailedDoublyLinkedList()) for j in range(self.n)] for i in range(self.n)]
        for q in self.quartets:
            #(i, j, k, l) = q
            gedges = self.green_edges(q)
            redges = self.green_edges(q)
            self.graph.add_edges_from(gedges, color='green', top=q) #maybe redundant
            self.graph.add_edges_from(redges, color='red', top=None)
            
            # update number of red egdes
            for (x,y) in redges:
                self.red[x][y] += 1
                self.red[y][x] += 1

            #update set of green edges
            for (u,v) in gedges:
                (a,b) = self.green[u][v]
                b.append(q)
                (c,d) = self.green[v][u]
                d.append(q)
        return

    def make_edis(self):
        self.edis = {}
        
        # dendropy requires taxa to be strings :(
        for i in range(self.n):
            leaf = dendropy.Tree(taxon_namespace=self.names)
            leaf.taxon = names.get_taxon(str(i))
            # assert tree.taxon_namespace is not trees.taxon_namespace
            self.edis[i] = leaf
        return

    def make_candidates(self):
        self.candidates = structs.TailedDoublyLinkedList()
        for i in range(self.n):
            for j in range(self.n):
                (ptr1,li1) = self.green_edges[i][j]
                # check if edge is a candidate
                if b.isntEmpty() and self.red_edges == 0: 
                    self.candidates.append((i,j))
                    (ptr2, li2) = self.green[j][i]
                    # have each green entry `point' to this newly added thing
                    # but is this a pointer ? will it change if i change the tail
                    # python confuses me
                    self.green[i][j] = (self.candidates.tail, li1)
                    self.green[j][i] = (self.candidates.tail, li2)
        return 

    def green_edges(self, q):
        (i, j, k, l) = q
        return [(i, j), (k, l)]

    def red_edges(self, q):
        (i, j, k, l) = q
        return [(i, k), (i,l), (j, k), (j, l)]
    
'''
------------------------------------------------------------------------------------------
                                      Stage 1 Helpers
                            (functions to help find a tree)
------------------------------------------------------------------------------------------
'''

    # dont know if we actually have to check green/red stuff
    # since the only way we add something to candidates is if we pass the check
    # (done)
    def find_siblings(self):
        curr = self.candidates.head
        while(curr is not None):
            (i, j) = curr.data
            if self.are_siblings(i, j):
                return (i, j)
            else:
                # disconnect ptrs in green_edges
                li1 = self.green_edges[i][j][1]
                li2 = self.green_edges[j][i][1]
                self.green_edges[i][j] = (None, li1)
                self.green_edges[j][i] = (None, li2)

                temp = curr 
                curr = curr.next
                self.candidates.delete(temp)
        return None

    # if a != null where (a,b) \in green_edges, check if i and j are editrees
    # done
    def are_siblings(self, i, j):
        (a,b) = self.green[i][j]
        if a != None: 
            if tree[i] != i or tree[j] != j:
                return False
            else:
                return True
        return False

    # note sure what this is meant to do; see delete_green_edge 
    def has_green_edge(self, i, j):
        (a,tddl) = self.green[i][j]
        node = tddl.head
        while node != None:
            q = node.data
            if self.is_ghost_edge(i, j, q):
                self.delete_green_edge(i,j,q)
                # node = tddl.delete(node)
            else:
                return True
        return False

    # done
    def is_ghost_edge(self, a, b, q):
        [c, d] = [x for x in q if x != a and x != b]
        return self.tree[c] == self.tree[d]

    # to deal with ghosts (?)
    # done
    def delete_green_edge(self, a, b, q):
        (ptr1, li1) = self.green[a][b]
        (ptr2, li2) = self.green[b][a]

        li1.delete_specific(q)
        li2.delete_specific(q)

        # ptr1 and ptr2 should always be pointing at the same guy in candidates
        if ptr1 is not None:
            if ptr1.data == (a,b) or ptr1.data == (b,a):
                self.candidates.delete(ptr1)
                self.candidates.delete(ptr2)

        return

    
    def update_structures(self, i, j):
        # first delete the red edges associated to e = (i, j)
        (ptr1, li1) = self.green_edges[i][j]
        curr = li1.head
        while (curr is not None):
            q = curr.data
            redges = self.red_edges(q)

            for (x,y) in redges:
                self.red_edges[x][y] -= 1
                self.red_edges[y][x] -= 1
                
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
        parent = dendropy.Tree(taxon_namespace=self.names)
        parent.taxon = self.names.get_taxon(str(i))
        parent.add_child(self.edis[i])
        parent.add_child(self.edis[j])
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

    # todo: need to also update candidates list...
    def update_colors(self, i, j):
        for k in range(self.n):
            if k != i:
                # update red
                redBefore = self.red[i][k]
                self.red[i][k] = self.red[i][k] + self.red[j][k]
                self.red[k][i] = self.red[k][i] + self.red[k][j]

                # deleting candidates 
                if redBefore == 0 and self.red[i][k] > 0: 
                    delCand = self.green[i][k][0]
                    self.candidates.delete(delCand)
                    self.green[i][k][0] = None
                    self.green[k][i][0] = None
                
                # update green
                greenBefore = self.green[i][k][1].length
                self.green[i][k][1] = self.green[i][k][1].union(self.green[i][j][1])
                self.green[k][i][1] = self.green[k][i][1].union(self.green[j][i][1])
                
                # inserting candidates 
                if greenBefore == 0 and self.green[i][k][1].length > 0:
                    self.candidates.append((i,k))
                    self.green[i][k][0] = self.candidates.tail
                    self.green[k][i][0] = self.candidates.tail


                # lets do this for safety
                self.red[j][k] = 0
                self.red[k][j] = 0
                self.green[j][k] = (None, structs.TailedDoublyLinkedList())
                self.green[k][j] = (None, structs.TailedDoublyLinkedList())
        return
                
'''
------------------------------------------------------------------------------------------
                                      Stage 2 Helpers
                            (functions to help verify the tree)
------------------------------------------------------------------------------------------
'''
    # returns distance and taxon of minimal closest leaf
    def get_rep(self, root):
        if root.is_leaf():
            return 0, int(root.taxon)
        child_reps = sorted([self.get_rep(child) for child in root.child_node_iter()])
        dist, name = child_reps[0]
        return dist+1, name

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
        # determine the representative element for each node
        for node in T.preorder_node_iter():
            reps[node] = self.get_rep(node)
        
        # constructs short quartet for each edge
        for edge in T.preorder_internal_edge_iter():
            head = edge.head_node
            tail = edge.tail_node
            # get children(?) of head
            i, j = [reps[child] for child in head.child_node_iter()]
            # if tail has no parent, the other part of the quartet is 
            # the reps of children of head's sibling
            # o.w. get one of head's siblings and tail's siblings
            if tail == T.seed_node:
                tail = self.get_other_child(tail, head)
                k, l= [reps[child] for child in tail.child_node_iter()]
            else:
                k = reps[self.get_other_child(tail, head)]
                parent = tail.parent_node
                l = reps[self.get_other_child(parent, tail)]
            rep_quartets.append((i, j, k, l))
        
        return rep_quartets

    # returns whether input quartet q is inside quartet list via binary search
    def in_quartets(self, q):
        # confused as to whether this works..
        i = bisect_right(self.quartets, q)
        # this used to say 'self.quartetes[i-1] == x' but idk what x is so i assume its supposed to be q
        return i != len(self.quartets)+1 and self.quartets[i-1] == q

    # returns list of quartets which induce same split as q
    def same_splits(self, q):
        i, j, k, l = q
        return [(i, j, k, l), (j, i, k, l), (i, j, l, k), (j, i, l, k)]
        
    def are_reps_in_quartets(self, rep_quartets):
        return all(any(in_quartets(q) for q in self.same_splits(rep)) for rep in rep_quartets)
    
    def are_quartets_in_tree(self, T):
        #https://www.geeksforgeeks.org/lca-for-general-or-n-ary-trees-sparse-matrix-dp-approach-onlogn-ologn/
        pass
