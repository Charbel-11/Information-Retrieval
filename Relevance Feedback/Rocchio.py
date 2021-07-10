import time
from IndexBuilder import InvertedIndexReader
from IndexBuilder import Preprocessor

queries = ["number theory", "all pairs shortest path", "useful data structures", "maximum matching in bipartite graphs",
           "flow"]

relevantDoc = [{3084}, {2972, 1629}, {1865}, {3159, 1651, 2761}, {1643, 2596, 1663}]

#Prints potential query expansion
def RocchioAlgorithm():
    postingLists = InvertedIndexReader.getInvertedIndexWithTfIdf()
    docs = InvertedIndexReader.getDocumentOrder()

    qIdx = 0
    for query in queries:
        start = time.time()

        termsID = {}
        curDocs = {}
        idx = 0
        words = Preprocessor.normalize(query)

        Q = []
        docsVectors = []

        for word in words:
            print(word, len(termsID), len(curDocs))
            if word not in termsID:
                termsID[word] = idx
                Q.append(1)
                for vectors in docsVectors:
                    vectors.append(0)
                idx += 1
            else:
                Q[termsID[word]] = 1

            if len(postingLists[word]) > 500:
                postingLists[word] = postingLists[word][:500]
                for relDocId in relevantDoc[qIdx]:
                    postingLists[word].append([1, relDocId])

            for pair in postingLists[word]:
                if pair[1] not in curDocs:
                    curDocs[pair[1]] = len(curDocs)
                    docsVectors.append([0 for i in range(idx)])
                curDocID = curDocs[pair[1]]

                curTerms = Preprocessor.getTokensFromHTMLDoc(docs[pair[1]])
                for term in curTerms:
                    if term not in termsID:
                        termsID[term] = idx
                        Q.append(0)
                        for vectors in docsVectors:
                            vectors.append(0)
                        idx += 1
                    docsVectors[curDocID][termsID[term]] = 1

        n = idx
        numRelevant = len(relevantDoc[qIdx])
        numIrrelevant = len(curDocs) - numRelevant

        idxToDocID = [0 for i in range(len(curDocs))]
        idxToTerm = ["" for i in range(len(termsID))]
        for term in termsID:
            idxToTerm[termsID[term]] = term
        for doc in curDocs:
            idxToDocID[curDocs[doc]] = doc

        QM = Q.copy()
        for i in range(len(curDocs)):
            factor = -1/numIrrelevant
            if idxToDocID[i] in relevantDoc[qIdx]:
                factor = 1/numRelevant
            for j in range(n):
                QM[j] += factor * docsVectors[i][j]

        for i in range(n):
            QM[i] = (max(0, QM[i]), i)
        QM.sort(reverse=True)
        for j in range(10):
            print(str(j+1) + " - " + idxToTerm[QM[j][1]] + " " + str(QM[j][0]))

        print("Ran in " + str(time.time() - start) + " s")

        qIdx += 1


RocchioAlgorithm()