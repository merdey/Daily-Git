#!/usr/bin/env python

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def compute(char):
  return (((ord(char) << 5) | (ord(char) >> 3)) ^ 111) & 255

verify_arr = [193, 35, 9, 33, 1, 9, 3, 33, 9, 225]
user_arr = []

for i in verify_arr:
  for char in alphabet:
    if compute(char) == i:
      print(char)
      break


