import Phrase_Queries
from IndexBuilder import Preprocessor
import time

queries = [
    "numbr theiry",
    "shortast path",
    "usefl data structures",
    "matchong biparfite graphs",
    "centrod decompositon"
]

#Returns an array containing all words with edit distance at most 2 with s
def generateCloseWords(s):
    ans = {s}

    def generateCloseWordsRec(cur, changes, s, i):
        if i >= len(s) and changes == 0:
            ans.add(cur)
            return

        if i < len(s):
            cur += s[i]
            generateCloseWordsRec(cur, changes, s, i + 1)
            cur = cur[:-1]
        if changes == 0:
            return

        for j in range(26):
            cur += chr(ord('a') + j)
            if i < len(s) and s[i] != chr(ord('a') + j):
                generateCloseWordsRec(cur, changes - 1, s, i + 1)  # Replace
            generateCloseWordsRec(cur, changes - 1, s, i)  # Add
            cur = cur[:-1]

        if i < len(s):
            generateCloseWordsRec(cur, changes - 1, s, i + 1)  # Delete

    generateCloseWordsRec("", 2, s, 0)
    return ans

# Given a 2D array, finds its cartesian product
def generateAllPossibleQueries(possibleWords):
    possibleQueries = []

    def generateAllPossibleQueriesRec(curQuery, i):
        if i == len(possibleWords):
            possibleQueries.append(curQuery)
            return

        initialQuery = curQuery
        for j in range(len(possibleWords[i])):
            if curQuery != "":
                curQuery += " "
            curQuery += possibleWords[i][j]
            generateAllPossibleQueriesRec(curQuery, i + 1)
            curQuery = initialQuery

    generateAllPossibleQueriesRec("", 0)
    return possibleQueries

def findPossibleQueriesWithEditDistance(query, dictionary):
    words = query.split(" ")
    possibleWords = []
    for word in words:
        curChoices = generateCloseWords(word)
        possibleWords.append([Preprocessor.stemmer.stem(x) for x in curChoices if
                              x not in Preprocessor.stopW and Preprocessor.stemmer.stem(x) in dictionary])
        possibleWords[len(possibleWords) - 1] = list(set(possibleWords[len(possibleWords) - 1]))

    return generateAllPossibleQueries(possibleWords)

#Generates the trigrams of a string s
def generateTrigrams(s):
    trigrams = []
    for i in range(len(s) - 2):
        trigrams.append(s[i:i+3])
    return trigrams

#Given a dictionary, it generates a list of each trigram with the words containing it
def generateTrigramsList(dictionary):
    trigramsList = {}
    for word in dictionary:
        curTrigrams = generateTrigrams(word)
        for tri in curTrigrams:
            if tri not in trigramsList:
                trigramsList[tri] = [word]
            elif trigramsList[tri][len(trigramsList[tri])-1] != word:
                trigramsList[tri].append(word)
    return trigramsList

#Given a word and a trigramsList, it returns the best 2 choices
def findTop2Candidates(s, trigramsList):
    trigrams = list(set(generateTrigrams(s)))
    relevantLists = [trigramsList[x] for x in trigrams]
    idx = [0 for i in range(len(relevantLists))]
    candidates = []

    cnt = 0
    while cnt < len(relevantLists):
        minIdx = []
        min = chr(ord('z')+1)
        for j in range(len(relevantLists)):
            if idx[j] >= len(relevantLists[j]):
                continue
            if relevantLists[j][idx[j]] < min:
                min = relevantLists[j][idx[j]]
                minIdx = [j]
            elif relevantLists[j][idx[j]] == min:
                minIdx.append(j)

        jacCoeff = len(minIdx)/(len(trigrams) + len(set(generateTrigrams(min))) - len(minIdx))
        candidates.append((jacCoeff, min))

        for i in minIdx:
            idx[i] += 1
            if idx[i] == len(relevantLists[i]):
                cnt += 1

    candidates.sort(reverse=True)
    if len(candidates) == 0:
        return []
    if len(candidates) == 1:
        return candidates[0][1]
    return [candidates[0][1], candidates[1][1]]

#Given a query, it returns the possible corrections
def findPossibleQueriesWithNGrams(query, trigramsList):
    possibleWords = []
    words = query.split(" ")
    for word in words:
        possibleWords.append(findTop2Candidates(word, trigramsList))

    return generateAllPossibleQueries(possibleWords)

#If type == 0, it uses edit distance
#If type == 1, it uses n-grams
def handleQueries(type):
    positionalIndex = Phrase_Queries.getPositionalIndex()
    avrgTime = 0

    if type == 1:
        trigramsList = generateTrigramsList(positionalIndex.keys())

    for q in queries:
        start_time = time.time()

        if type == 0:
            possibleQueries = findPossibleQueriesWithEditDistance(q, positionalIndex.keys())
        elif type == 1:
            possibleQueries = findPossibleQueriesWithNGrams(q, trigramsList)

        numMatches = []
        for pQ in possibleQueries:
            curMatches = Phrase_Queries.answerQueryUsingPositional(pQ, positionalIndex)
            numMatches.append((len(curMatches), pQ))

        numMatches.sort(reverse=True)
        print(numMatches[:3])

        curTime = time.time() - start_time
        print("The query \"" + q + "\" took " + str(curTime) + " s")
        avrgTime += curTime

    avrgTime /= 5
    print("A query took " + str(avrgTime) + " s on average")

#handleQueries(0)
handleQueries(1)