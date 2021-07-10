from IndexBuilder import Preprocessor
from scipy.sparse.linalg import svds, eigs
from scipy.sparse import csc_matrix
import numpy as np

m = 1000

def getDocumentOrder():
    f = open("Document Order.txt", "r", encoding="utf-8")
    d = []
    for line in f:
        d.append(line[:-1])
    return d

#Generates the pairs (term, docID) for all documents given their paths
def generateTermsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    for path in paths:
        tokens = Preprocessor.getTokensFromHTMLDoc(path)
        for token in tokens:
            termsToDoc.append([token, docID])
        docID += 1
    return termsToDoc

def buildTermIncidenceMatrix():
    paths = Preprocessor.getAllHTMLFiles('C:\Website-Collections\Competitive Programming Tutorials')
    termsToDoc = generateTermsDocIDMap(paths)
    n=len(paths)

    freq = {}
    for pair in termsToDoc:
        if pair[0] not in freq:
            freq[pair[0]] = 1
        freq[pair[0]] += 1

    freq = list(sorted(freq.items(), key=lambda item: item[1]))

    topTerms = {}
    for i in range(m):
        topTerms[freq[len(freq) - 1 - i][0]] = i

    A = [[0 for j in range(n)] for i in range(m)]
    for pair in termsToDoc:
        if not pair[0] in topTerms:
            continue
        A[topTerms[pair[0]]][pair[1]] = 1

    f = open("TopTerms.txt", "w", encoding="utf-8")
    for term in topTerms:
        f.write(term)
        f.write('\n')
    f.close()

    f = open("TermIncidenceMatrix.txt", "w", encoding="utf-8")
    for row in A:
        strRow = [str(x) for x in row]
        f.write(" ".join(strRow))
        f.write('\n')
    f.close()

def getTopTerms():
    f = open("TopTerms.txt", "r", encoding="utf-8")
    topTerms = {}
    i = 0
    for word in f:
        word = word[:-1]
        topTerms[word] = i
        i += 1
    f.close()
    return topTerms

def readIncidenceMatrix():
    f = open("TermIncidenceMatrix.txt", "r", encoding="utf-8")
    A = []
    for row in f:
        row = row.split(" ")
        nums = [int(x) for x in row]
        A.append(nums)
    return A


queries = ["number theori",
           "pair shortest path",
           "use data structur",
           "maximum match bipartit graph",
           "flow"]

def LTI():
    Atmp = readIncidenceMatrix()
    topTerms = getTopTerms()
    docOrder = getDocumentOrder()
    k=140
    alpha = 0.3

    A=csc_matrix(Atmp, dtype=float)
    u, sVal, vt = svds(A)
    uk, skVal, vtk = svds(A, k)
    A = np.matrix(Atmp)

    s=[[0 for i in range(len(sVal))] for j in range(len(sVal))]
    for i in range(len(sVal)):
        s[i][i] = sVal[i]

    sk = [[0 for i in range(len(skVal))] for j in range(len(skVal))]
    for i in range(len(skVal)):
        sk[i][i] = skVal[i]

    u=np.matrix(u)
    s=np.matrix(s)
    vt=np.matrix(vt)
    uk=np.matrix(uk)
    sk=np.matrix(sk)
    vtk=np.matrix(vtk)

    for query in queries:
        query = query.split(" ")
        q = [0 for i in range(m)]
        for word in query:
            if word not in topTerms:
                continue
            q[topTerms[word]] = 1

        qT = np.matrix(q)
        q = np.transpose(qT)
        qkT = np.matmul(np.matmul(qT, uk), sk)

        scores = alpha*np.matmul(qT, A) + (1-alpha)*np.matmul(qkT, vtk)
        scores = scores.tolist()[0]

        revDoc = []
        for i in range(len(scores)):
            revDoc.append([scores[i], i])
        revDoc.sort(reverse=True)

        print(query)
        for i in range(5):
            print(docOrder[revDoc[i][1]])

def termAssociation():
    Atmp = readIncidenceMatrix()
    topTerms = getTopTerms()
    topTermsRev = [0 for x in range(m)]
    for term in topTerms:
        topTermsRev[topTerms[term]] = term
    k = 340

    A = csc_matrix(Atmp, dtype=float)
    u, sVal, vt = svds(A)
    uk, skVal, vtk = svds(A, k)
    A = np.matrix(Atmp)

    s = [[0 for i in range(len(sVal))] for j in range(len(sVal))]
    for i in range(len(sVal)):
        s[i][i] = sVal[i]

    sk = [[0 for i in range(len(skVal))] for j in range(len(skVal))]
    for i in range(len(skVal)):
        sk[i][i] = skVal[i]

    u = np.matrix(u)
    s = np.matrix(s)
    vt = np.matrix(vt)
    uk = np.matrix(uk)
    sk = np.matrix(sk)
    vtk = np.matrix(vtk)

    ck = np.matmul(uk, np.transpose(uk))
    ck = ck.tolist()
    n = len(ck)
    vals = []
    for i in range(n):
        if topTermsRev[i][0] < 'a' or topTermsRev[i][0] > 'z':
            continue
        for j in range(i + 1, n):
            if topTermsRev[j][0] < 'a' or topTermsRev[j][0] > 'z':
                continue
            vals.append([ck[i][j], i, j])

    vals.sort(reverse=True)
    for i in range(50):
        print(topTermsRev[vals[i][1]], topTermsRev[vals[i][2]])

termAssociation()

