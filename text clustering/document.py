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

    def update(self, new_word_counts):
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
