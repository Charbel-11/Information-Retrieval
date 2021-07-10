#Creates an inverted index out of a directory containing HTML files (i.e., webpages)

from io import StringIO
from html.parser import HTMLParser
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem.porter import *
import os
import re
import nltk
import html2text

nltk.download('punkt')
nltk.download('stopwords') 

directoryPath = 'C:\Website-Collections\Competitive Programming Tutorials'

#Returns an array containing the paths of all HTML files in the cur directory
def getAllHTMLFiles(curDir):
    paths = []
    for curPath, folders, files in os.walk(curDir):
        for file in files:
            if (re.search(r".html$", file)):
                paths.append(os.path.join(curPath, file))
    return paths

#Generates the text file that contains the docs in order
def generateDocMap(paths):
    f = open("Document Order.txt", "w", encoding="utf-8")
    for path in paths:
        f.write(path + '\n')
    f.close()

#HTML Stripping code; It removes all HTML related text from an HTML file
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()
def stripTags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Generates the pairs (term, docID) for all documents given their paths
def generateTermsDocIDMap(paths):
    termsToDoc = []
    docID = 0
    stemmer = PorterStemmer()
    stopW = set(stopwords.words('english'))

    for path in paths:
        curFile = open(path, "r", encoding="utf-8")
        curData = curFile.read()
        curFile.close()

        # (REMOVE <SCRIPT> to </script> and variations)
        pattern = r'<[ ]*script.*?\/[ ]*script[ ]*>'  # mach any char zero or more times
        curData = re.sub(pattern, '', curData, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        # (REMOVE HTML <STYLE> to </style> and variations)
        pattern = r'<[ ]*style.*?\/[ ]*style[ ]*>'  # mach any char zero or more times
        curData = re.sub(pattern, '', curData, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        curData = stripTags(curData)    #Remove HTML data
        curData = curData.lower()       #Everything becomes lowercase
        curData = re.sub('[^\w\s]+', ' ', curData)  #Remove punctuation
        initialTokens = word_tokenize(curData) #Tokenize
        tokens = [stemmer.stem(word) for word in initialTokens if len(word) > 1 and not word in stopW] #Remove Stop Words & stem the token
        
        for token in tokens:
            termsToDoc.append((token, docID))
        
        docID += 1
    
    return termsToDoc

#Given a dictionary term -> docIDs, we store it in a text file as
#term: freqID ID1, ID2, ..., IDn
def storePostingLists(postingLists):
    f = open("Inverted Indexes.txt", "w", encoding="utf-8")
    for post in postingLists:
        f.write(post + ": ")
        f.write(str(len(postingLists[post])) + " ")
        f.write(", ".join([str(i) for i in postingLists[post]]))
        f.write('\n')
    f.close()

def generateInvertedIndex():
    paths = getAllHTMLFiles(directoryPath)
    generateDocMap(paths)

    termsToDoc = generateTermsDocIDMap(paths)
    termsToDoc = list(dict.fromkeys(termsToDoc))
    termsToDoc.sort()
    
    postingLists = {}
    for pair in termsToDoc:
        if (pair[0][0] < 'a' or pair[0][0] > 'z'):
            continue
        
        if pair[0] not in postingLists:
            postingLists[pair[0]] = []
        postingLists[pair[0]].append(pair[1])

    storePostingLists(postingLists)

generateInvertedIndex()
