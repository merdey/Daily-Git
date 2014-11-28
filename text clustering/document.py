from bs4 import BeautifulSoup
import nltk, requests

class Document:
    def __init__(self, title, word_counts={}):
        self.title = title
        self.word_counts = word_counts
        self.length = len(word_counts)
        
        self.words = set()
        for word in word_counts:
            self.words.add(word)

    def frequency(self, word):
        if word in self.word_counts:
            return self.word_counts[word] / self.length
        return 0

    def add(self, new_word_counts):
        for word in new_word_counts:
            if word in self.word_counts:
                self.word_counts[word] += new_word_counts[word]
            else:
                self.word_counts[word] = new_word_counts[word]
                self.words.add(word)
        self.length += len(new_word_counts)

def distance(doc_a, doc_b):
    distance = 0
    all_words = doc_a.words | doc_b.words
    for word in all_words:
        distance += abs(doc_a.frequency(word) - doc_b.frequency(word))
    return distance

def documentFromUrl(url):
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
    return Document(url, word_counts)
