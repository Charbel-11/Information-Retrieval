from io import StringIO
from html.parser import HTMLParser
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
import os
import re

#nltk.download('punkt')
#nltk.download('stopwords')

stopW = set(stopwords.words('english'))
stemmer = PorterStemmer()
patternScript = r'<[ ]*script.*?\/[ ]*script[ ]*>'
patternStyle = r'<[ ]*style.*?\/[ ]*style[ ]*>'

# HTML Stripping code; It removes all HTML related text from an HTML file
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()
def stripTags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Normalizes the given strings and returns its corresponding tokens
def normalize(curData):
    curData = curData.lower()  # Everything becomes lowercase
    curData = re.sub('[^\w\s]+', ' ', curData)  # Remove punctuation
    initialTokens = word_tokenize(curData)  # Tokenize
    tokens = [stemmer.stem(word) for word in initialTokens if
              len(word) > 1 and not word in stopW]  # Remove Stop Words & stem the token

    return tokens

#Returns a tokenized version of the HTML document present at path
def getTokensFromHTMLDoc(path):
    curFile = open(path, "r", encoding="utf-8")
    curData = curFile.read()
    curFile.close()

    # (REMOVE <SCRIPT> to </script> and variations)
    curData = re.sub(patternScript, ' ', curData, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
    # (REMOVE HTML <STYLE> to </style> and variations)
    curData = re.sub(patternStyle, ' ', curData, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
#    curData = html2text.html2text(curData)
    curData = stripTags(curData)  # Remove HTML data

    return normalize(curData)

#Returns an array containing the paths of all HTML files in the cur directory
def getAllHTMLFiles(curDir):
    paths = []
    for curPath, folders, files in os.walk(curDir):
        for file in files:
            if (re.search(r".html$", file)):
                paths.append(os.path.join(curPath, file))
    return paths