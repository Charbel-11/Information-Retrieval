import time
from IndexBuilder import InvertedIndexReader
from IndexBuilder import Preprocessor

queries=[
    "number theory",
    "all pairs shortest path",
    "useful data structures",
    "maximum matching in bipartite graphs",
    "min cost flow"
]

#Returns consecutive pairs in a query after normalizing the words
def getConsecutivePairs(s):
    tokens = Preprocessor.normalize(s)
    pairs = []
    for i in range(len(tokens)-1):
        pairs.append((tokens[i], tokens[i+1]))
    return pairs

#Checks whether target is in the corresponding document
def checkInDoc(target, docPath):
    doc = " ".join(Preprocessor.getTokensFromHTMLDoc(docPath))
    return target in doc

#Finds the intersection of and and b
def intersection(a, b):
    i = 0
    j = 0
    ans = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ans.append(a[i])
            i+=1
            j+=1
        elif a[i] < b[j]:
            i+=1
        else:
            j+=1
    return ans

def answerQueriesUsingBiwords():
    invertedIndex = InvertedIndexReader.getBiwordInvertedIndex()
    docOrder = InvertedIndexReader.getDocumentOrder()

    avrgTime = 0
    for q in queries:
        start_time = time.time()
        queryPairs = getConsecutivePairs(q)
        ans = invertedIndex[queryPairs[0]]
        for i in range(1, len(queryPairs)):
            ans = intersection(ans, invertedIndex[queryPairs[i]])

        target = " ".join(queryPairs[0])
        for i in range(1, len(queryPairs)):
            target += " " + queryPairs[i][1]

        print("Documents matching " + q + ": ")
        for id in ans:
            id = int(id)
            if checkInDoc(target, docOrder[id]):
                print(docOrder[id])

        avrgTime += time.time()-start_time

    avrgTime/=5
    print("With biwords, it took " + str(avrgTime) + " seconds per query on average")

def answerQueriesUsingPositional():
    docOrder = InvertedIndexReader.getDocumentOrder()
    positionalIndexes = InvertedIndexReader.getPositionalIndex()

    avrgTime = 0
    for q in queries:
        start_time = time.time()

        print("Documents matching " + q + ": ")
        matches = answerQueryUsingPositional(q, positionalIndexes)
        for match in matches:
            print(docOrder[match])

        avrgTime += time.time() - start_time

    avrgTime/=5
    print("With positional indexes, it took " + str(avrgTime) + " seconds per query on average")

#Takes a query and the positional indices and return an array of doc IDs matching the query
def answerQueryUsingPositional(q, positionalIndexes):
    terms = Preprocessor.normalize(q)
    n = len(terms)

    if not terms[0] in positionalIndexes:
        return []
    candidates = positionalIndexes[terms[0]].keys()
    for i in range(1, n):
        if not terms[i] in positionalIndexes:
            return []
        candidates = candidates & positionalIndexes[terms[i]].keys()

    if n == 1:
        return candidates

    matches = []
    for docID in candidates:
        idx = [0 for i in range(n)]
        positions = []
        for i in range(n):
            positions.append(positionalIndexes[terms[i]][docID])

        i = 1
        OK = False
        while idx[0] < len(positions[0]):
            while idx[i] < len(positions[i]) and positions[i][idx[i]] <= positions[i - 1][idx[i - 1]]:
                idx[i] += 1
            if idx[i] == len(positions[i]):
                break
            if positions[i][idx[i]] == 1 + positions[i - 1][idx[i - 1]]:
                i += 1
                if i == n:
                    OK = True
                    break
            else:
                idx[0] += 1
                i = 1

        if OK:
            matches.append(docID)

    return matches

answerQueriesUsingPositional()
