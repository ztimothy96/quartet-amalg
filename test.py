import structs
import watc
import datagen
import dendropy

def test_from_file(n):
    outPath = "quartet-files/" + str(num_sequences) + "-from-1000L1-R0/"
    filePath = outPath + "quarts.txt"
    quarts = datagen.regenQuarts(filePath)
    tree_finder = watc.WATC(num_sequences, quarts)
    T = tree_finder.find_some_tree()
    return T

#test on a perfectly consistent input; easiest case
def test_on_tree(n, T):
    lca = structs.LCA(T.seed_node)
    quartets = []
    for i in range(n):
        for j in range(i):
            for k in range(j):
                for l in range(k):
                    lj, lk, ll = lca.query(i, j), lca.query(i, k), lca.query(i, l)
                    if lj == lk:
                        q = ((i, l), (j, k))
                    elif lj == ll:
                        q = ((i, k), (j, l))
                    elif lk == ll:
                        q = ((i, j), (k, l))
                    else:
                        raise ValueError('invalid tree topology')
                    quartets.append(q)
    tree_finder = watc.WATC(n, quartets)
    T = tree_finder.find_some_tree()
    return T
                
def make_caterpillar(n):
    tree = dendropy.Tree()
    curr = tree.seed_node
    for i in range(n-1):
        leaf = curr.new_child(label = str(i))
        curr = curr.new_child(label = str(i+n))
    leaf = curr.new_child(label = str(n-1))
    return tree

n = 10
cat = make_caterpillar(n)
T = test_on_tree(n, cat)
