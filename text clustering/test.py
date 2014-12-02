from multiprocessing import Pool
from document import *
from bookmark_conversion import *
import time

def testReadTimings(trials, num_of_urls):
    unsorted = bookmarksToUrls('Profile 1')[:num_of_urls] #little patience
    print('read in bookmarks')
    seq_time, multi_time, multi_time2 = 0, 0, 0
    for i in range(trials):
        seq_time += timeRead(sequentialRead, unsorted)
        multi_time += timeRead(multiRead, unsorted)
        multi_time2 += timeRead(ludicrousRead, unsorted)

    print("Average sequential read time: " + str(seq_time / trials))
    print("Average threaded read time: " + str(multi_time / trials))
    print("Average ludicrous read time: " + str(multi_time2 / trials))
    print("Multi-read speed up = " + str(seq_time / multi_time))
    print("Ludicrous-read speed up = " + str(seq_time / multi_time2))
    input("Press enter to continue")

def sequentialRead(urls):
    unsorted_docs = [documentFromUrl(url) for url in urls]
    return unsorted_docs

def multiRead(urls):
    with Pool(processes=4) as pool:
        unsorted_docs = pool.map(documentFromUrl, urls)
    return unsorted_docs

def ludicrousRead(urls):
    pool_size = 6
    with Pool(processes=pool_size) as pool:
        unsorted_docs = pool.map(documentFromUrl, urls)
    return unsorted_docs

def timeRead(f, urls):
    time_taken = 0
    trials = 3
    for i in range(trials):
        start = time.clock()
        f(urls)
        end = time.clock()
        time_taken += (end - start)
    print(time_taken)
    return time_taken
