import structs
import watc
import datagen
import dendropy

#filePath = "quartet-files/from-sim-B/sim-B-640/quarts.txt"

# tests tree reconstruction on caterpillar
def test_cat(size):
    quarts = [((a, b), (c, d)) for d in range(size) for c in range(d) for b in range(c) for a in range(b)]
    tf = watc.WATC(size, quarts)
    T = tf.get_tree()
    print(T)

def test_from_file(filePath, size):
    quarts = datagen.regenQuarts(filePath)
    tf = watc.WATC(size, quarts)
    T = tf.get_tree()
    print(T)

# tests on arbitrary labeled tree, using all correct induced quartets
def test_from_tree(tree):
    quarts = get_quartets_from_tree(tree)
    size = len(tree.leaf_nodes())
    tf = watc.WATC(size, quarts)
    T = tf.get_tree()
    print(T)

def label_all_nodes(tree):
    i = 0
    j = 0
    n = len(tree.leaf_nodes())
    for leaf in tree.leaf_nodes():
        leaf.label = str(i)
        i += 1
    for node in tree.internal_nodes():
        node.label = str(n + j)
        j += 1

# returns all induced quartets on leaves in a tree
def get_quartets_from_tree(tree):
    lca = structs.LCA(tree.seed_node)
    quarts = []
    n= len(tree.leaf_nodes())
    for i in range(n):
        for j in range(i):
            for k in range(j):
                for l in range(k):
                    li = int(tree.leaf_nodes()[i].label)
                    lj = int(tree.leaf_nodes()[j].label)
                    lk = int(tree.leaf_nodes()[k].label)
                    ll = int(tree.leaf_nodes()[l].label)
                    q = ((ll, lk), (lj, li))
                    quarts.append(lca.get_quartet(q))
    return quarts

get_label = lambda node: node.label

sB = "((raccoon:19.19959,bear:6.80041):0.84600,((sea_lion:11.99700, seal:12.00300):7.52973,((monkey:100.85930,cat:47.14069):20.59201, weasel:18.87953):2.09460):3.87382,dog:25.46154);"
TB = dendropy.Tree.get_from_string(sB, schema="newick")
label_all_nodes(TB)
print(TB.as_ascii_plot(node_label_compose_fn = get_label))
quarts = get_quartets_from_tree(TB)
size = len(TB.leaf_nodes())
tf = watc.WATC(size, quarts)
T = tf.get_tree()


# test_cat(10)

