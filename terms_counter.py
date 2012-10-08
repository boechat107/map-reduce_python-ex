#!/usr/bin/python
# -*- coding: utf-8 -*-

# ========================================================================================= 
# Author: Andre A. Boechat
# File: terms_counter.py
# Date: October 01, 2012, 08:35:27 PM
# Description: Homework of module 3 of the Coursera's Big Data course.
# 
# Reference:
#     https://www.coursera.org/course/bigdata
#     https://github.com/michaelfairley/mincemeatpy
# ========================================================================================= 


# ========================================================================================= 
# Getting the homework data
# ========================================================================================= 
import os

data_folder = "hw3data"
file_list = [os.path.join(data_folder,f) for f in os.listdir(data_folder)]

def fileContens(filename):
    f = open(filename)
    try:
        return f.read()
    finally:
        f.close()

datasource = dict(enumerate((fileContens(fname) for fname in file_list)))

# ========================================================================================= 
# MAP and REDUCE functions
# ========================================================================================= 

def mapfn(filenumber, filecontent):
    from utils import normalize_words
    ## Emits all the contents for each author
    author_contents = {}
    for line in filecontent.splitlines():
        ## conf:::author_1::author2:::title
        docdata = line.split(':::')
        authors_list = docdata[1].split('::')
        title = docdata[-1]
        for author in authors_list:
            author = normalize_words(author)
            if author_contents.has_key(author):
                author_contents[author] = author_contents[author] + " " + title
            else:
                author_contents[author] = title
    ## Map results
    for author in author_contents.keys():
        yield author, author_contents[author]

def reducefn(author, titles):
    from stopwords import allStopWords
    from utils import normalize_words
    terms_freq = {}
    for title in titles:
        ### Main tasks to do: normalize words (lower case), delete stopwords, punctuation,
        ### hyphens, single letter words and count the cumulative frequency.
        title_terms = normalize_words(title)
        for term in title_terms.split():
            ## allStopWords comes from stopwords file.
            ## Single letter words are removed.
            if not (allStopWords.has_key(term) or len(term) == 1):
                if terms_freq.has_key(term):
                    terms_freq[term] = terms_freq[term] + 1
                else:
                    terms_freq[term] = 1
    ## Reduce results.
    return terms_freq

# ========================================================================================= 
# mincemeat client configuration
# ========================================================================================= 
import mincemeat

s = mincemeat.Server()
s.datasource = datasource #dict([datasource.popitem(), datasource.popitem()])
s.mapfn = mapfn
s.reducefn = reducefn

# ========================================================================================= 
# Results
# ========================================================================================= 
from time import time

starttime = time()
results = s.run_server(password="changeme")
endtime = time()
print endtime - starttime
## CSV like printing
for author in results.keys():
    print author + ";",
    words = results[author]
    sortedwords = sorted(words.items(), key=lambda x: x[1], reverse=True)
    for wordtuple in sortedwords:
        print wordtuple[0] + ":", wordtuple[1], "; ",
    print

