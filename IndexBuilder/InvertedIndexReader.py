def getDocumentOrder():
    f = open("Document Order.txt", "r", encoding="utf-8")
    d = []
    for line in f:
        d.append(line[:-1])
    return d

def getInvertedIndexWithTfIdf():
    f = open("Inverted Indexes.txt", "r", encoding="utf-8")
    postingLists = {}

    for line in f:
        line = line[:-1] + ", "
        termList = line.split(": ")
        word = termList[0]
        postingList = termList[1].split("], ")
        postingList = postingList[:-1]
        postingList[0] = postingList[0].split(" ", 1)[1]
        postingList = [(a[1:]).split(", ") for a in postingList]
        for p in postingList:
            p[0] = float(p[0])
            p[1] = int(p[1])
        postingLists[word] = postingList

    f.close()
    return postingLists

def getBiwordInvertedIndex():
    f = open("Biword Inverted Indexes.txt", "r", encoding="utf-8")
    biwords = {}
    for line in f:
        line = line[:-1]
        termList = line.split(": ")
        words = termList[0].split(", ")
        postingList = termList[1].split(", ")
        postingList[0] = postingList[0].split(" ")[1]
        postingList = [int(a) for a in postingList]
        biwords[(words[0], words[1])] = postingList
    f.close()
    return biwords

def getPositionalIndex():
    f = open("Positional Indexes.txt", "r", encoding="utf-8")
    data = f.readlines()
    f.close()

    positionalIndexes = {}
    i = 0
    while i < len(data):
        term = data[i][:-1]
        positionalIndexes[term] = {}
        i += 1
        freqID = int(data[i][:-1])
        i += 1
        for j in range(freqID):
            positions = data[i][:-1].split(", ")
            positions = [int(x) for x in positions]
            docID = positions[0]
            positions = positions[1:]
            positionalIndexes[term][docID] = positions
            i += 1

    return positionalIndexes

