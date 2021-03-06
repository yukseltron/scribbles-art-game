#!/usr/bin/env python
# coding: utf-8

# In[47]:


# importing the hashlib module
import hashlib
# importing random module
import random

#create function to generate a seed from file hash
def getHash(filename):

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return seeded random function using file hash as seed
   return int(h.hexdigest(), 16)
