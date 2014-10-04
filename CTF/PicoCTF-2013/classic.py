table = {'m': 'e', 'c': 't'}

def decipher(string):
    d = ''
    for letter in string:
        if letter in table:
            letter = table[letter]
        d += letter
    return d

def letterCount(string):
    counts = {}
    for letter in string:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1
    for letter in counts:
        counts[letter] = counts[letter] / len(string)
    return counts

string = 'cslcehesehft ohrumvc zmvm scmk ht ptohmte ehbmc mxmt eufsju eumq pvm dshem mpchgq lvfymt zheu nsce p rmtohg ptk rprmv, fv bfvm vmomtegq lq ofbbft ofbrsemvhwmk effgc. qfsv ymq hc: zumt_kf_zm_jme_ef_eum_upvk_cesii'
print('letter counts ' + str(letterCount(string)))
print('original ' + string)
print('current attempt ' + decipher(string))
        
