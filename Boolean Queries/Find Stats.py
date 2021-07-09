#Gives some insights about an inverted index

import matplotlib.pyplot as plt

def numberOfLines(docName):
    return sum(1 for line in open(docName, "r", encoding="utf-8"))

def getPostingLists():
    f = open("Inverted Indexes.txt", "r", encoding="utf-8")
    postingLists = {}
    for line in f:
        (word, listData) = line.split(': ')
        (size, postingList) = listData.split(' ', 1)
        curList = postingList.split(', ')
        postingLists[word] = [(int)(post) for post in curList]
    f.close()
    return postingLists

distWords = numberOfLines("Inverted Indexes.txt")
docs = numberOfLines("Document Order.txt")
print("Number of distinct words = " + str(distWords))
print("Number of documents = " + str(docs))

uniqueWordInDocFreq = {}    #docId->#unique words
postingLists = getPostingLists()
for word in postingLists:
    for docID in postingLists[word]:
        if docID not in uniqueWordInDocFreq:
            uniqueWordInDocFreq[docID] = 0 
        uniqueWordInDocFreq[docID] += 1
        
ss = 0
for docID in uniqueWordInDocFreq:
    ss += uniqueWordInDocFreq[docID]
ss/=len(uniqueWordInDocFreq)
        
print("The average number of distinct words in a doc is " + str(ss) + "\n") 

docFreq = []
freqVal = 0
for word in postingLists:
    n = len(postingLists[word])
    freqVal += n
    docFreq.append((n, word))

print("A term appears in " + str(freqVal/distWords) + " documents on average")

docFreq.sort()
x = []
y = []
for t in docFreq:
    x.append(t[1])
    y.append(t[0])
plt.bar(x, y)
plt.xticks(rotation = -90)
plt.gcf().subplots_adjust(bottom=0.15)
plt.ylim(1800)
plt.show()
    
