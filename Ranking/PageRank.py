import re
import numpy as np
import time
from IndexBuilder import Preprocessor
from IndexBuilder import InvertedIndexReader

def getAllHyperlinks(path):
    curFile = open(path, "r", encoding="utf-8")
    curData = curFile.read()
    curFile.close()

    mainDir = path
    for j in range(len(mainDir)-1, 0, -1):
        if mainDir[j] == '\\':
            mainDir = mainDir[:j]
            break

    hyperlinks = []
    pattern = re.compile("\\bhref=\"([^\"]+)\"")
    for link in re.findall(pattern, curData.lower()):
        link = link.replace("/", "\\")
        link = link.replace("\\\\", "\\")
        curDir = mainDir
        while len(link) > 3 and link[0] == '.' and link[1] == '.' and link[2] == '\\':
            link = link[3:]
            for j in range(len(curDir)-1, 0, -1):
                if curDir[j] == '\\':
                    curDir = curDir[:j]
                    break

        link = curDir + "\\" + link
        hyperlinks.append(link)

    return hyperlinks

#A[i][j] = 1 if doc i has a link to doc j
def createGraph(paths, dir):
    n = len(paths)
    A = [[0 for i in range(n)] for j in range(n)]

    pathToID = {}
    for i in range(n):
        pathToID[paths[i]] = i

    idx = 0
    for path in paths:
        links = getAllHyperlinks(path)
        for link in links:
            if link in pathToID:
                A[idx][pathToID[link]] = 1
        idx += 1

    return A

#A is taken by reference, so it is modified
def modifyAdjMatrix(A):
    n = len(A)
    alpha = 0.15

    rowSum = [0 for i in range(n)]
    for i in range(n):
        for j in range(n):
            rowSum[i] += A[i][j]

    for i in range(n):
        all0 = True
        for j in range(n):
            if A[i][j] != 0:
                all0 = False
                break

        if all0:
            for j in range(n):
                A[i][j] = 1/n
        else:
            for j in range(n):
                A[i][j] /= rowSum[i]

    for i in range(n):
        for j in range(n):
            A[i][j] *= (1-alpha)
            A[i][j] += alpha/n

def findPageRank(dir):
    paths = Preprocessor.getAllHTMLFiles(dir)
    docs = InvertedIndexReader.getDocumentOrder()
    A = createGraph(paths, dir)

    numLinks = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] == 1:
                numLinks += 1
    print("There are " + str(numLinks) + " links")

    modifyAdjMatrix(A)

    n = len(A)
    R = [1/n for i in range(n)]

    start = time.time()
    iterations = 0

    maxChange = 1
    eps = 0.0001
    while maxChange > eps:
        iterations += 1
        maxChange = 0
        newR = np.matmul(R, A)
        c = 1/(sum(newR))
        for i in range(n):
            newR[i] *= c
            maxChange = max(maxChange, abs(newR[i] - R[i]))
        R = newR

    print("It converged in " + str(time.time()-start) + "s after " + str(iterations) + " iterations")

    docRankIDPair = []
    for i in range(n):
        docRankIDPair.append((R[i], i))
    docRankIDPair.sort(reverse=True)

    for i in range(10):
        print(str(i+1) + " - " + str(docRankIDPair[i][0]) + " " + docs[docRankIDPair[i][1]])
    print()

    return docRankIDPair
