import os
import sys
import itertools
import numpy

import dendropy
from dendropy.calculate.treecompare \
    import false_positives_and_negatives

class Sequence:
    def __init__(self, tag, seq, cid):
        self.tag = tag
        self.seq = seq
        self.id = cid

'''
===============================================================================
                FUNCTIONS FOR READING and REGENERATING
===============================================================================
'''
# Modified a bit from Vlad's; num_sequences is which sequences you want to 
def readFromFasta(num_sequences, filePath, removeDashes = False):
    sequences = {}
    currentSequence = None
    currentID = 0
    with open(filePath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if currentID >= num_sequences:
                    break
                tag = line[1:]
                currentSequence = Sequence(tag, "", currentID)
                sequences[currentID] = currentSequence
                currentID += 1
            else :
                if(removeDashes):
                    line = line.replace("-", "")
                currentSequence.seq = currentSequence.seq + line
    print(str(len(sequences)))
    print(str(num_sequences))

    assert(len(sequences) == num_sequences)
    print("Read " + str(len(sequences)) + " sequences from " + filePath + " ..")
    return sequences


# input a dist.txt and output (n,dist) where n is the number of sequences and dist is the distance matrix
# have not tested
def regenDistanceMatrix(filePath):
    dist = []
    i = 0

    with open(filePath) as f:
        for line in f:
            if line.startswith('['):
                line.replace('[',"")
                line.replace(']',"")
                row = line.split(", ")
                dist[i] = row 
                i += 1
    return (len(dist),dist)

# input a seq-ids.txt and output dictionary where index of a sequence name is what its alias'd to
# have not tested
def regenSeqIDDict(filePath):
    seq_dict = {}
    with open(filePath) as f:
        for line in f:
            line = line.replace("\n","")
            line = line.replace("(","")
            line = line.replace(")","")
            temp = line.split(",")
            n = int(temp[0])
            print(str(n))
            seq_dict[n] = temp[1]
    return seq_dict

# input a quarts.txt and output list of quartets in the form ((a,b),(c,d))
def regenQuarts(filePath):
    quarts = []
    with open(filePath) as f:
        for line in f:
            line = line.replace("(","")
            line = line.replace(")","")
            temp = line.split(",")
            a, b, c, d = [int(i) for i in temp]
            quarts.append(((a, b), (c, d)))
        
    return quarts


'''
===============================================================================
                        FUNCTIONS FOR WRITING
===============================================================================
'''

# Function to write distance matrix to text file (for later?)
def writeDistToFile(matrix, filename):
    n = len(matrix)
    with open(filename, 'w') as outfile:
        for i in range(n):
            outfile.write(str(matrix[i]))
            outfile.write("\n\n\n")
    return


def writeQuartsToFile(quarts,filename):
    with open(filename,'w') as outfile:
        for ((a,b),(c,d)) in quarts:
            outfile.write("((" + str(a) + "," + str(b) + "),(" + str(c) + "," + str(d) + "))\n")
    return

# for QMC 
def writeQuartsToFileWithRealName(quarts,seq_dict, filename):
    with open(filename, 'w') as outfile:
        for ((a,b),(c,d)) in quarts:
            na = seq_dict[a].tag
            nb = seq_dict[b].tag
            nc = seq_dict[c].tag
            nd = seq_dict[d].tag
            outfile.write(str(na)+ "," + str(nb) + "|" + str(nc) + "," + str(nd) + " ")

def writeQuartsToFileQMC(quarts, filename):
    with open(filename, 'w') as outfile:
        for ((a,b),(c,d)) in quarts:
            outfile.write(str(a)+ "," + str(b) + "|" + str(c) + "," + str(d) + " ")

def writeSeqIDsToFile(seq_dict,filename):
    with open(filename,'w') as outfile:
        for key in seq_dict:
            outfile.write("(" + str(key) + "," + seq_dict[key].tag + ")\n")
    return

def genReadMe(num_seqs, seq_length, readFrom, filename):
    with open(filename,'w') as outfile:
        outfile.write("This folder uses " + str(num_seqs) + " sequences  of length " + str(seq_length) + " from\n" + readFrom)
        outfile.write("\n\nseq-ids.txt: contains names and indices of sequences")
        outfile.write("\ndist.txt: n x n jcdist distance matrix")
        outfile.write("\nquarts.txt: printed list of quartets generated using 4PM on distance matrix in dist.txt")
    
    return

'''
===============================================================================
                  FUNCTIONS TO COMPUTE QUARTET TREES (naively)
=============================================================================== 
'''

# Computes normalized hamming distance between two sequences that are of the same length. 
def hammingDist(str1,str2):
    n = len(str1)
    c = 0
    for i in range(n):
        if str1[i] != str2[i]:
            c += 1
    
    return c/n


# Computes the distance matrix between sequences using hammingDist
def distMatrix(sequences, n):
    distances = [ [ 0 for i in range(n) ] for j in range(n) ] 

    for i in range(n):
        for j in range(i,n):
            # maybe we consider doing another distance metric bc this seems meh
            hamming = hammingDist(sequences[i].seq,sequences[j].seq)
            mid = 1 - ((4/3)*hamming)
            if (mid <= 0):
                jcdist = float("inf")
            else: 
                jcdist = (-3/4)*numpy.log(mid)
            distances[i][j] = jcdist
            distances[j][i] = jcdist
        
    return distances



def fourPointMethod(matrix):
    n = len(matrix)
    quarts = []
    for (a,b,c,d) in itertools.combinations(range(n),4):
        sum1 = matrix[a][b] + matrix[c][d]
        sum2 = matrix[a][c] + matrix[b][d]
        sum3 = matrix[a][d] + matrix[b][c]

        if sum1 <= sum2 and sum1 <= sum3: 
            quarts.append(((a,b),(c,d)))
        elif sum2 <= sum1 and sum2 <= sum3:
            quarts.append(((a,c),(b,d)))
        elif sum3 <= sum1 and sum3 <= sum2:
            quarts.append(((a,d),(b,c)))

    return quarts

'''
===============================================================================
                    tree fixin
===============================================================================
'''

def renameNodes(tree, seq_dict):
    for leaf in tree.leaf_nodes():
        new_label = seq_dict[int(leaf.taxon.label)]
        leaf.taxon.label = new_label
    return tree


'''
===============================================================================
                    what C programs would call "main"
===============================================================================
'''

if __name__ == "__main__":
    
    thing_to_run = 1
    conditions = ['L1','L2','M1','M2','M3','S1','S2']
    
    if thing_to_run == 1:
        for cond in conditions:
            for i in range(10):
                replicateNo = "R" + str(i)
                seq_path = "/Users/tanvibajpai/Desktop/AGB/quartet-files/100" + cond + "/" + replicateNo + "/seq-ids.txt"
                seq_dict = regenSeqIDDict(seq_path)
                tree_path = "/Users/tanvibajpai/Desktop/AGB/trees-to-compare/100" + cond + "/" + replicateNo + "/MXCNtree.dat"
                tax = dendropy.TaxonNamespace()
                tr1 = dendropy.Tree.get(path=tree_path,
                                            schema='newick',
                                            rooting='force-unrooted',
                                            taxon_namespace=tax)
                print(tr1)
                print(tax)
                '''for leaf in tr1.leaf_node_iter():
                    print(leaf)'''
                new_tree = renameNodes(tr1,seq_dict)
                put_tree_path = "/Users/tanvibajpai/Desktop/AGB/trees-to-compare/100" + cond + "/" + replicateNo + "/qmc.tt"
                new_tree.write(path = put_tree_path,schema = "newick")

    elif thing_to_run == 2:
        seq_length = 0
        num_sequences = 100
        for cond in conditions:
            for i in range(10):
                replicateNo = "R" + str(i)

                readFrom = "/Users/tanvibajpai/Desktop/AGB/data/100" + cond + "/100" + cond + "/" + replicateNo + "/rose.aln.true.fasta"
                outPath = "/Users/tanvibajpai/Desktop/AGB/quartet-files/100" + cond + "/" + replicateNo + "/"

                genReadMe(num_sequences,seq_length,readFrom,outPath + "README.txt")
                seq_dict = readFromFasta(num_sequences, readFrom)
                writeSeqIDsToFile(seq_dict,outPath + "seq-ids.txt")

                distance_matrix = distMatrix(seq_dict, num_sequences)
                writeDistToFile(distance_matrix, outPath + "dist.txt")

                quarts = fourPointMethod(distance_matrix)
                writeQuartsToFile(quarts,outPath + "quarts.txt")
                writeQuartsToFileQMC(quarts,outPath + "quartQMC1.txt")
                #writeQuartsToFileWithRealName(quarts,seq_dict,outPath + "quartQMC.txt")



    '''
    seq_length = 10
    num_sequences = 32
    sim_letter = "C"

    while seq_length <= 640:
        readFrom = "datasets/sim-" + sim_letter + "/sim-" + sim_letter + "-" + str(seq_length) + "/test-" + sim_letter + "-" + str(seq_length) + ".fas"
        outPath = "quartet-files/from-sim-" + sim_letter + "/sim-" + sim_letter + "-" + str(seq_length) + "/"

        genReadMe(num_sequences,seq_length,readFrom,outPath + "README.txt")

        seq_dict = readFromFasta(num_sequences,readFrom)
        writeSeqIDsToFile(seq_dict,outPath + "seq-ids.txt")

        distance_matrix = distMatrix(seq_dict, num_sequences)
        writeDistToFile(distance_matrix, outPath + "dist.txt")

        quarts = fourPointMethod(distance_matrix)
        writeQuartsToFile(quarts,outPath + "quarts.txt")

        seq_length *= 2

    '''



