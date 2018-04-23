#!/usr/local/bin/python

import os
import re
import sys
import textract
import tensorflow as tf
from collections import defaultdict
from fnmatch import fnmatch

BASE =40
N = 3

def doc2ngram(text):
    for i in range(N, len(text)):
        yield text[i-N: i]

def ngram2id(ngram):
    b = 1
    num = 0

    for i,c in enumerate(ngram.lower()):
        if c >= '0' and c <= '9':
            k = ord(c) - ord('0')
        elif c >= 'a' and c <= 'z':
            k = ord(c) - ord('a') + 10
        else: 
            print c
        num = num + b * k
        b = b * BASE
    return num

def doc2vec(text):
    idx = defaultdict(int)
    for t in doc2ngram(text):
        idx[ngram2id(t)] += 1
    
    indices = []
    values = []
    
    for t,v in idx.items():
        indices.append([t,0])
        values.append(v)
    dim = BASE ** N
    print dim
    vec = tf.SparseTensor(indices=indices, values=values, dense_shape=[BASE ** N, 1])
    return vec



text = "000zzzZZZaaa000EmpfansscheinRec"

for t in doc2ngram(text):
    print "%s" % t
    print "%s %d" %(t, ngram2id(t))

print doc2vec(text)
