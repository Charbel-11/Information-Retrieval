import matplotlib.pyplot as plt
import numpy as np
from IndexBuilder import Preprocessor

def getKMostFrequent(k):
    paths = Preprocessor.getAllHTMLFiles('C:\Website-Collections\Competitive Programming Tutorials')

    freqD = {}
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for token in tokens:
            if token[0] < 'a' or token[0] > 'z':
                continue
            if token not in freqD:
                freqD[token] = 0
            freqD[token] += 1

    freqA = []
    for term in freqD:
        freqA.append((freqD[term], term))

    freqA.sort(reverse=True)
    for i in range(k):
        print(str(i+1) + ") " + freqA[i][1] + " " + str(freqA[i][0]))

    x = []
    y = []
    rank = 1
    for pair in freqA:
        x.append(rank)
        rank += 1
        y.append(pair[0])

    plt.figure(1)
    plt.plot(np.log(x), np.log(y), label="Observed points")
    plt.xlabel("log(rank)")
    plt.ylabel("log(collection frequency)")

    # Gets the proportion of terms that appear less than 5 times in the collection
    numTerms = len(freqD)
    numRareTerms = 0
    for term in freqD:
        if freqD[term] < 5:
            numRareTerms += 1

    print("Words that occur fewer than 5 times consist of " + str(numRareTerms/numTerms) + " the total number terms")

    #cf_i=K/i -> log(cf_i) = log(K) - log(i)
    K = freqA[0][0]
    xT = np.log(x)
    yT = []
    for i in range(len(freqA)):
        yT.append(np.log(K) - np.log(i+1))

    plt.figure(2)
    plt.plot(np.log(x), np.log(y), label="Observed points")
    plt.plot(xT, yT, label="Zipf's Law Line")
    plt.xlabel("log(rank)")
    plt.ylabel("log(collection frequency)")
    plt.legend()
    plt.show()

getKMostFrequent(25)




