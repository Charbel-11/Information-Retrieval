from IndexBuilder import Preprocessor
import matplotlib.pyplot as plt
import numpy as np
import random

# Divides the array into n parts
def partitionArray(A, n):
    blockLen = int(len(A)/n)
    partitions = []
    for i in range(n):
        cur = []
        for j in range(blockLen):
            cur.append(A[i * blockLen + j])
        if i == n-1:
            j = i * blockLen + blockLen
            while j < len(A):
                cur.append(A[j])
                j += 1
        partitions.append(cur)
    return partitions

#Plots the log-log relation between number of tokens (x-axis) and number of unique terms (y-axis)
def plotMTRelation():
    paths = Preprocessor.getAllHTMLFiles('C:\Website-Collections\Competitive Programming Tutorials')
    random.shuffle(paths)
    docBlock = partitionArray(paths, 20)

    tokenBlock = []
    termBlock = []
    tokenPts = []
    termPts = []

    numTokens = 0
    dictionary = set()
    for block in range(20):
        for path in docBlock[block]:
            curTokens = Preprocessor.getTokensFromHTMLDoc(path)
            numTokens += len(curTokens)
            for token in curTokens:
                dictionary.add(token)
            tokenPts.append(numTokens)
            termPts.append(len(dictionary))
        tokenBlock.append(numTokens)
        termBlock.append(len(dictionary))

    plt.plot(np.log(tokenBlock), np.log(termBlock), 'o', label="Original Data")
    plt.xlabel("Log(number of tokens)")
    plt.ylabel("Log(number of unique terms)")

    target = len(dictionary) * 0.3
    idx = 0
    while termPts[idx] < target:
        idx += 1
    print("For 30% of the vocabulary to be encountered, " + str((tokenPts[idx]/numTokens)*100) + "% of the tokens must be read")

    #Finding the least square fit
    A = np.vstack([np.log(tokenBlock), np.ones(len(tokenBlock))]).T
    m, c = np.linalg.lstsq(A, np.log(termBlock), rcond=None)[0]
    plt.plot(np.log(tokenBlock), np.log(tokenBlock)*m+c, label="Fitted Line")
    plt.legend()
    plt.show()

    print("Slope: " + str(m) + "  " + "intercept: " + str(c))

    print("Total number of tokens: " + str(numTokens))
    print("Total number of terms: " + str(len(dictionary)))

plotMTRelation()