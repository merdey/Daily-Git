#!/usr/bin/env python
import sys

alphaL = "abcdefghijklnmopqrstuvqxyz"
alphaU = "ABCDEFGHIJKLMNOPQRSTUVQXYZ"
num    = "0123456789"
keychars = num+alphaL+alphaU

#if len(sys.argv) != 3:
#  print "Usage: %s SECRET_KEY PLAINTEXT"%(sys.argv[0])
#  sys.exit()

#key = sys.argv[1]
#if not key.isalnum():
#  print "Your key is invalid, it may only be alphanumeric characters"
#  sys.exit()

#plaintext = sys.argv[2]

#key = 'T0pS3cre7key'
#ciphertext = ""
#for i in range(len(plaintext)):
#  rotate_amount = keychars.index(key[i%len(key)])
#  if plaintext[i] in alphaL:
#    enc_char = ord('a') + (ord(plaintext[i])-ord('a')+rotate_amount)%26
#  elif plaintext[i] in alphaU:
#    enc_char = ord('A') + (ord(plaintext[i])-ord('A')+rotate_amount)%26
#  elif plaintext[i] in num:
#    enc_char = ord('0') + (ord(plaintext[i])-ord('0')+rotate_amount)%10
#  else:
#    enc_char = ord(plaintext[i])
#  ciphertext = ciphertext + chr(enc_char)

def encrypt(plaintext, key):
  ciphertext = ''
  for i in range(len(plaintext)):
    rotate_amount = keychars.index(key[i%len(key)])
  if plaintext[i] in alphaL:
    enc_char = ord('a') + (ord(plaintext[i])-ord('a')+rotate_amount)%26
  elif plaintext[i] in alphaU:
    enc_char = ord('A') + (ord(plaintext[i])-ord('A')+rotate_amount)%26
  elif plaintext[i] in num:
    enc_char = ord('0') + (ord(plaintext[i])-ord('0')+rotate_amount)%10
  else:
    enc_char = ord(plaintext[i])
#  ciphertext = ciphertext + chr(enc_char)

def decipher(ciphertext, key):
  plaintext = ''
  for i in range(len(ciphertext)):
    rotate_amount = keychars.index(key[i%len(key)])
    if ciphertext[i] in alphaL:
      d = ord('a')
    elif ciphertext[i] in alphaU:
      d = ord('A')
    elif ciphertext[i] in num:
      d = ord('0')
    else:
      d = ord(ciphertext[i])
    plaintext += chr(d)
  return plaintext
    

key = 'T0pS3cre7key'
ciphertext = 'Bot kmws mikferuigmzf rmfrxrwqe abs perudsf! Nvm kda ut ab8bv_w4ue0_ab8v_DDU'
print(decipher(ciphertext, key))
#print "Encryption complete, ENC(%s,%s) = %s"%(plaintext,key,ciphertext)
