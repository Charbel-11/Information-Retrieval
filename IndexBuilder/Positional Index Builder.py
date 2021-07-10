import Preprocessor

directoryPath = 'C:\Website-Collections\Competitive Programming Tutorials'

def generateTermsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for i in range(len(tokens)):
            termsToDoc.append((tokens[i], docID, i))
        docID += 1

    return termsToDoc

#Given a term -> docIDs -> positions, we store it in a text file as
#term
#freqID
#ID1, pos1ID1, pos2ID1, ...
#ID2, pos1ID2, pos2ID2, ...
#...
def storePositionalPostingLists(postingLists):
    f = open("Positional Indexes.txt", "w", encoding="utf-8")
    for post in postingLists:
        f.write(post + '\n')
        f.write(str(len(postingLists[post])) + '\n')
        for docID in postingLists[post]:
            f.write(str(docID) + ", ")
            f.write(", ".join([str(i) for i in postingLists[post][docID]]))
            f.write('\n')
    f.close()

def generatePositionalInvertedIndex():
    paths = Preprocessor.getAllHTMLFiles(directoryPath)

    termsToDoc = generateTermsDocIDMap(paths)
    termsToDoc.sort()

    postingLists = {}
    for entry in termsToDoc:
        w = entry[0]
        docID = entry[1]
        if w[0] < 'a' or w[0] > 'z':
            continue

        if w not in postingLists:
            postingLists[w] = {}
        if docID not in postingLists[w]:
            postingLists[w][docID] = []
        postingLists[w][docID].append(entry[2])

    storePositionalPostingLists(postingLists)

generatePositionalInvertedIndex()