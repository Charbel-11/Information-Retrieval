import Preprocessor

directoryPath = 'C:\Website-Collections\Competitive Programming Tutorials'

# Generates the text file that contains the docs in order
def generateDocMap(paths):
    f = open("Document Order.txt", "w", encoding="utf-8")
    for path in paths:
        f.write(path + '\n')
    f.close()


# Generates the pairs (term, docID) for all documents given their paths
def generateTermsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for token in tokens:
            termsToDoc.append((token, docID))
        docID += 1
    return termsToDoc


# Generates the pairs ((term0, term1), docID) for all documents given their paths
def generateBiwordsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for i in range(len(tokens) - 1):
            termsToDoc.append(((tokens[i], tokens[i + 1]), docID))
        docID += 1
    return termsToDoc


# Given a dictionary term -> docIDs, we store it in a text file as
# term: freqID ID1, ID2, ..., IDn
def storePostingLists(postingLists):
    f = open("Inverted Indexes.txt", "w", encoding="utf-8")
    for post in postingLists:
        f.write(post + ": ")
        f.write(str(len(postingLists[post])) + " ")
        f.write(", ".join([str(i) for i in postingLists[post]]))
        f.write('\n')
    f.close()


# Given a biword -> docIDs, we store it in a text file as
# term1, term2: freqID ID1, ID2, ..., IDn
def storeBiwordPostingLists(postingLists):
    f = open("Biword Inverted Indexes.txt", "w", encoding="utf-8")
    for post in postingLists:
        pair = ", ".join([post[0], post[1]])
        f.write(pair + ": ")
        f.write(str(len(postingLists[post])) + " ")
        f.write(", ".join([str(i) for i in postingLists[post]]))
        f.write('\n')
    f.close()


def generateBiwordInvertedIndex():
    paths = Preprocessor.getAllHTMLFiles(directoryPath)
    generateDocMap(paths)

    termsToDoc = generateBiwordsDocIDMap(paths)
    termsToDoc = list(dict.fromkeys(termsToDoc))
    termsToDoc.sort()

    postingLists = {}
    for pair in termsToDoc:  # pair contains ((w0, w1), docID) since termsToDoc is an array, not a dict
        w1 = pair[0][0]
        w2 = pair[0][1]
        if w1[0] < 'a' or w1[0] > 'z' or w2[0] < 'a' or w2[0] > 'z':
            continue

        if pair[0] not in postingLists:
            postingLists[pair[0]] = []
        postingLists[pair[0]].append(pair[1])

    storeBiwordPostingLists(postingLists)


def generateInvertedIndex():
    paths = Preprocessor.getAllHTMLFiles(directoryPath)
    generateDocMap(paths)

    termsToDoc = generateTermsDocIDMap(paths)
    termsToDoc = list(dict.fromkeys(termsToDoc))
    termsToDoc.sort()

    postingLists = {}
    for pair in termsToDoc:
        if pair[0][0] < 'a' or pair[0][0] > 'z':
            continue

        if pair[0] not in postingLists:
            postingLists[pair[0]] = []
        postingLists[pair[0]].append(pair[1])

    storePostingLists(postingLists)
