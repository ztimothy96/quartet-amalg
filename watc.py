import dendropy
import networkx as nx
import structs

# convert all taxa to integers 0 through n-1
# n = number of taxa
# code skeleton so far

class WATC:
    def __init__(self, n, quartets):
        self.n = n
        self.quartets = quartets
        self.make_colorful_things()
        self.make_edis()
        self.tree = range(n)
        self.make_candidates() #doubly linked list
        return

    def get_tree(self):
        T = self.find_some_tree()
        if self.verify_tree(T):
            return T
        else:
            return "Fail"

    def find_some_tree(self):
        m = len(self.edis)
        while m >= 4:
            if m == 4:
                pass #brute force the base case
            else:
                i, j = self.find_siblings()
                self.update_structures(i, j)
                pass #merge two edi-trees
        pass
    
    def verify_tree(self, T):
        #https://www.geeksforgeeks.org/lca-for-general-or-n-ary-trees-sparse-matrix-dp-approach-onlogn-ologn/
        pass

    #constructor functions
    def make_colorful_things(self):
        self.graph = nx.Multigraph()
        self.graph.add_nodes_from(range(0, self.n))
        self.red = [[0 for j in range(self.n)] for i in range(self.n)]
        self.green = [[( (None, structs.TailedDoublyLinkedList()) for j in range(self.n)] for i in range(self.n)]
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
        self.edis = dendropy.TreeList()
        names = dendropy.TaxonNamespace([str(i) for i in range(self.n)])
        # dendropy requires taxa to be strings :(
        for i in range(self.n):
            leaf = dendropy.Tree(taxon_namespace=names)
            leaf.taxon = names.get_taxon(str(i))
            # assert tree.taxon_namespace is not trees.taxon_namespace
            self.edis.append(leaf)
        return

    # indexing may be off
    # (done)
    def make_candidates(self):
        self.candidates = structs.TailedDoublyLinkedList()
        for i from 1 to n:
            for j from i to n:
                (ptr1,li1) = self.green_edges[i][j]
                # check if edge is a candidate
                if b.isntEmpty() and self.red_edges == 0: 
                    self.candidates.append((i,j))
                    (ptr2, li2) = self.green_edges[j][i]
                    # have each green entry `point' to this newly added thing
                    # but is this a pointer ? will it change if i change the tail
                    # python confuses me
                    self.green_edges[i][j] = (self.candidates.tail, li1)
                    self.green_edges[j][i] = (self.candidates.tail, li2)
        return 



    #actually finding a tree
    # dont know if we actually have to check green/red stuff
    # since the only way we add something to candidates is if we pass the check
    # (done)
    def find_siblings(self):
        curr = self.candidates.head
        while(curr is not None):
            (i, j) = curr.data
            if are_siblings(i, j):
                return (i, j)
            else:
                # "disconnect" ptrs in green_edges
                (ptr1, li1) = self.green_edges[i][j]
                (ptr2, li2) = self.green_edges[j][i]
                self.green_edges[i][j] = (None, li1)
                self.green_edges[j][i] = (None, li2)

                temp = curr 
                curr = curr.next
                self.candidates.delete(temp)
        return "No sibling was found; sadness"

    # if a != null where (a,b) \in green_edges, check if i and j are editrees
    # done
    def are_siblings(self, i, j):
        (a,b) = self.green_edges[i][j]
        if a != None: 
            if tree[i] != i or tree[j] != j:
                return False
            else:
                return True
        return False

    # note sure what this is meant to do; see delete_green_edge 
    def has_green_edge(self, i, j):
        tddl = self.green[i][j]
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
        (ptr1, li1) = self.green_edges[a][b]
        (ptr2, li2) = self.green_edges[b][a]

        li1.delete_specific(q)
        li2.delete_specific(q)

        # ptr1 and ptr2 should always be pointing at the same guy in candidates
        if ptr1 is not None:
            if ptr1.data == (a,b) or ptr1.data == (b,a):
                self.candidates.delete(ptr1)
                self.candidates.delete(ptr2)

        return

    
    def update_structures(self, i, j):
        # first process every green edge e in green_ij and green_ji 
        # by deleting the four red edges associated to e
        (ptr1, li1) = self.green_edges[i][j]
        curr = li1.head
        while (curr is not None):
            q = curr.data
            redges = self.red_edges(q)

            for((x,y) in redges):
                self.red_edges[x][y] -= 1
                self.red_edges[y][x] -= 1

        # then we merge two edisubtrees into one (do this in different func?)
        pass

    def green_edges(self, q):
        (i, j, k, l) = q
        return [(i, j), (k, l)]

    def red_edges(self, q):
        (i, j, k, l) = q
        return [(i, k), (i,l), (j, k), (j, l)]


    #verification functions here... maybe implement the actual data structures first
