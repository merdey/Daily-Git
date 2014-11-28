from bs4 import BeautifulSoup
from document import Document, distance
import nltk, requests

urls = ['http://www.crummy.com/software/BeautifulSoup/bs4/doc/',
        'http://en.wikipedia.org/wiki/Cluster_analysis',
        'http://www.nltk.org/book/'
        ]

clusters = []
documents = []
for url in urls:
    r = requests.get(url)
    source = r.text
    soup = BeautifulSoup(source)
    raw = soup.get_text()
    
    #create a somewhat sanitized list of words
    words = [token.lower() for token in nltk.word_tokenize(raw) if token.isalpha() and len(token) > 3]

    #count words and create new document
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    d = Document(url, word_counts)
    documents.append(d)

