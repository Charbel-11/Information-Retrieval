import Preprocessor
import numpy as np

directoryPath = 'C:\Website-Collections\Competitive Programming Tutorials'

#Generates the text file that contains the docs in order
def generateDocMap(paths):
    f = open("Document Order.txt", "w", encoding="utf-8")
    for path in paths:
        f.write(path + '\n')
    f.close()

#Generates the pairs (term, docID) for all documents given their paths
def generateTermsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for token in tokens:
            termsToDoc.append((token, docID))
        docID += 1
    return termsToDoc

# Given a dictionary term -> docIDs, we store it in a text file as
# term: freqID [score1, ID1], [score2, ID2], ..., [scoren, IDn]
def storePostingLists(postingLists):
    f = open("Inverted Indexes.txt", "w", encoding="utf-8")
    for post in postingLists:
        f.write(post + ": ")
        f.write(str(len(postingLists[post])) + " ")
        f.write(", ".join([str(i) for i in postingLists[post]]))
        f.write('\n')
    f.close()

# Given a dictionary term -> docIDs, we store it in a text file as
# term ID1 score1 ID2 score2 ... IDn scoren
def storePostingLists2(postingLists):
    f = open("InvertedIndexTFIDF.txt", "w", encoding="utf-8")
    for post in postingLists:
        f.write(post + " ")
        f.write(" ".join([str(i[1]) + " " + str(i[0]) for i in postingLists[post]]))
        f.write('\n')
    f.close()


def generateInvertedIndexWithTfIdfScore():
    paths = Preprocessor.getAllHTMLFiles(directoryPath)
    generateDocMap(paths)

    termsToDoc = generateTermsDocIDMap(paths)
    termFreq = {}
    for pair in termsToDoc:
        if pair not in termFreq:
            termFreq[pair] = 0
        termFreq[pair] += 1

    #Remove duplicates and sort
    termsToDoc = list(dict.fromkeys(termsToDoc))
    termsToDoc.sort()

    postingLists = {}
    for pair in termsToDoc:
        if pair[0][0] < 'a' or pair[0][0] > 'z':
            continue

        if pair[0] not in postingLists:
            postingLists[pair[0]] = []
        postingLists[pair[0]].append([1 + np.log10(termFreq[pair]), pair[1]])

    #Multiply term frequencies by idf to get the tf-idf score
    for term in postingLists:
        N = len(paths)
        idf = np.log10(N/len(postingLists[term]))
        for docList in postingLists[term]:
            docList[0] *= idf
        postingLists[term].sort(reverse=True)

    storePostingLists2(postingLists)

generateInvertedIndexWithTfIdfScore()