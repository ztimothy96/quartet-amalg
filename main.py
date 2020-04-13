import os
import sys

import dendropy
from dendropy.calculate.treecompare \
    import false_positives_and_negatives

# function provided by Vlad Smirnov
def readFromFasta(filePath, removeDashes = False):
 sequences = {}
 currentSequence = None
 with open(filePath) as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            tag = line[1:]
            currentSequence = Sequence(tag, "")
            sequences[tag] = currentSequence
        else :
            if(removeDashes):
                line = line.replace("-", "")
            currentSequence.seq = currentSequence.seq + line
 print("Read " + str(len(sequences)) + " sequences from " + filePath + " ..")
 return sequences



#this is me making sure my python is configured properly

msg = "whats good in the hood"
print(msg)

print("oh also hello world")



