from bs4 import BeautifulSoup
from corpus import *
from cluster import *
from document import *
import nltk, requests, operator

#creates clusters with predefined documents
cluster_definitions = {'Python': ['https://www.python.org/',
                                  'http://en.wikipedia.org/wiki/Python_(programming_language)',
                                  'http://learnpythonthehardway.org/book/'
                                  ],
                       'Gaming': ['http://kotaku.com/',
                                  'http://www.gamespot.com/',
                                  'http://www.ign.com/'
                                  ]
                      }
corpus = Corpus()
clusters = []
for cluster_name, urls in cluster_definitions.items():
    cluster_docs = []
    for url in urls:
        print('reading ' + url)
        cluster_docs.append(documentFromUrl(url, corpus))
    clusters.append(Cluster(cluster_name, cluster_docs))

while(True):
    response = input('Enter a url or -1 to quit: ')
    if response == '-1':
        break
    else:
        doc = documentFromUrl(response, corpus)
        distances = {}
        for cluster in clusters:
            distances[cluster] = distance(doc, cluster.corpus, corpus)

        matched_cluster = min(distances.items(), key=operator.itemgetter(1))[0]
        print('Belongs to: ' + matched_cluster.name)
        matched_cluster.update(doc)
