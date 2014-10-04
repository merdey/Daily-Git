import hashlib

dictionary = open('cain.txt', 'r')
dictionary_text = dictionary.read()
words = dictionary_text.split()
salt = '8058'
hashed = '03318769a5ee1354f7479acc69755e7c'

for word in words:
    key_hash = hashlib.md5(word + salt).hexdigest()
    if key_hash.startswith('c16'):
        print(key_hash, word)
        if key_hash == hashed:
            print('found')
            break
