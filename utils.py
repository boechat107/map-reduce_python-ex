#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import re

def normalize_words(wordsStr):
    ### Main tasks to do: normalize words (lower case), delete stopwords, punctuation, 
    ### hyphens, single letter words and count the cumulative frequency. 
    ## Removing diacritics
    unicode_nkfd = unicodedata.normalize('NFKD', unicode(wordsStr, 'utf-8'))
    wordsStr_ascii = unicode_nkfd.encode('ASCII', 'ignore')
    ## Removing apostrophe and converting to lower case.
    normStr = re.sub(r"['-]", '', wordsStr_ascii.lower())
    ## Removing punctuation.
    normStr = re.sub(r'[^0-9a-z]+', ' ', normStr)
    return normStr


