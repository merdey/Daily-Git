from bs4 import BeautifulSoup
import nltk, requests

class Document:
    def __init__(self, name, word_counts={}):
        self.name = name
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

    def remove(self, word_counts):
        for word in word_counts:
            self.word_counts[word] -= word_counts[word]
        self.length -= len(word_counts)

def distance(doc_a, doc_b, corpus):
    distance = 0
    all_words = doc_a.words | doc_b.words
    for word in all_words:
        idf = corpus.idf(word)
        adjusted_a = doc_a.frequency(word) * idf
        adjusted_b = doc_b.frequency(word) * idf
        distance += abs(adjusted_a - adjusted_b)
    return distance

def documentFromUrl(url, corpus):
    #reads text from url and creates document while keeping corpus counts updated
    try:
        r = requests.get(url)
        source = r.text
        soup = BeautifulSoup(source)
        raw = soup.get_text()
        
        #create a somewhat sanitized list of words
        words = [token.lower() for token in nltk.word_tokenize(raw) if token.isalpha()]

        #count words and create new document
        word_counts = {}
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        doc = Document(url, word_counts)
        corpus.addDocument(doc)
        return doc
    except:
        print('Could not create document from url')
