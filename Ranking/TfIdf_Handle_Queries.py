from datetime import datetime
import numpy as np
from IndexBuilder import InvertedIndexReader
from IndexBuilder import Preprocessor

queries = ["number theory", "all pairs shortest path", "useful data structures", "maximum matching in bipartite graphs",
           "flow"]

queriesModified = ["number theory polynomial", "all pairs shortest path Floyd Warshall", "useful data structures",
                   "maximum matching in bipartite graphs Hopcroft Karp", "flow augmenting residual"]

def handleQueryWithTfIdfRanking(query, postingLists, docs):
    print(query + ": ")
    query = Preprocessor.normalize(query)

    docScore = {}
    for word in query:
        curList = postingLists[word]
        for docVal in curList:
            if docVal[1] not in docScore:
                docScore[docVal[1]] = 0
            docScore[docVal[1]] += docVal[0]

    invertedDocVal = []
    for doc in docScore:
        invertedDocVal.append([docScore[doc], doc])
    invertedDocVal.sort(reverse=True)

    for i in range(min(5, len(invertedDocVal))):
        print(str(i + 1) + " -", end=" ")
        print(str(invertedDocVal[i][0]) + ", " + docs[invertedDocVal[i][1]] + " " + str(invertedDocVal[i][1]))

    return invertedDocVal


def handleQueriesWithTfIdfRanking(queries):
    postingLists = InvertedIndexReader.getInvertedIndexWithTfIdf()
    docs = InvertedIndexReader.getDocumentOrder()

    for query in queries:
        start_time = datetime.now().microsecond
        handleQueryWithTfIdfRanking(query, postingLists, docs)
        timeTaken = datetime.now().microsecond - start_time
        print(str(timeTaken) + " ms")
        print('\n')


def computeNDCG(docsRelevance):
    idx = 0
    print("NDCG@5: ")
    for docRelevance in docsRelevance:
        print(queries[idx] + ": ", end = " ")

        IDCG = docRelevance.copy()
        IDCG.sort(reverse=True)
        for i in range(1, len(IDCG)):
            IDCG[i] = IDCG[i-1] + IDCG[i]/np.log2(i+1)

        NDCG5 = docRelevance[0]
        for i in range(1, len(docRelevance)):
            NDCG5 += docRelevance[i]/np.log2(i+1)

        NDCG5 /= IDCG[4]
        print(NDCG5)

        idx += 1

#handleQueries(queries)
#computeNDCG([[2,0,0,1,1], [2,1,2,1,0], [1,0,0,1,2], [2,2,2,1,1], [2,2,1,1,2]])

#handleQueries(queriesModified)
#computeNDCG([[2,2,1,1,0], [1,2,2,1,1], [1,0,0,1,2], [2,2,2,2,1], [2,2,2,1,2]])