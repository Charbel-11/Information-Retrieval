from IndexBuilder import InvertedIndexReader
import PageRank
import TfIdf_Handle_Queries
import time

queries = ["number theory", "all pairs shortest path", "useful data structures", "maximum matching in bipartite graphs",
           "flow"]

#Uses both tf-idf and PageRank to rank documents
def handleQueriesWithPageRankAndTfIdf():
    docRankIDPair = PageRank.findPageRank("C:\Website-Collections\Competitive Programming Tutorials")
    pageRank = [0 for i in range(len(docRankIDPair))]
    for i in range(len(docRankIDPair)):
        pageRank[docRankIDPair[i][1]] = docRankIDPair[i][0]

    postingLists = InvertedIndexReader.getInvertedIndexWithTfIdf()
    docs = InvertedIndexReader.getDocumentOrder()

    for query in queries:
        startT = time.time()
        docScore = TfIdf_Handle_Queries.handleQueryWithTfIdfRanking(query, postingLists, docs)
        c = 0
        for i in range(len(docScore)):
            c += docScore[i][0]
        for i in range(len(docScore)):
            docScore[i][0] /= c
            docScore[i][0] = 0.5 * docScore[i][0] + 0.5 * pageRank[i]

        docScore.sort(reverse = True)
        print("Hybrid " + query)
        for i in range(5):
            print(str(i+1) + " " + str(docScore[i][0]) + " " + docs[docScore[i][1]])

        print("It took " + str(time.time() - startT) + " s")
        print()
