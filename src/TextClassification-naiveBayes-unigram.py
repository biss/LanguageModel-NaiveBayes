'''
Created on 19-Aug-2015
automatic text based language classification system for 3 Latin languages

@author: biswajeet
'''

import re
import sys
from decimal import *

getcontext().prec = 20  #precesion of the probabilities

#initialising the dictionaries
dictionary_eng = {}
dictionary_deu = {}
dictionary_fra = {}

dictionary_test = {}

#this method constructs/updates dictionary based on the corpus label
def construct_dictionary(array, doc_class):
    doc = str(doc_class) #corpus label
    
    #english corpus
    if (doc == 'eng'):
        for word in array:
            if(word != ''):
                if (word in dictionary_eng):
                    dictionary_eng[word] += 1
                else:
                    dictionary_eng[word] = 1
        print "corpus added in english dictionary"
        
    #german corpus
    if (doc == 'deu'):
        for word in array:
            if(word != ''):
                if (word in dictionary_deu):
                    dictionary_deu[word] += 1
                else:
                    dictionary_deu[word] = 1
        print "corpus added in german dictionary"

    #french corpus
    if (doc == 'fra'):
        for word in array:
            if(word != ''):
                if (word in dictionary_fra):
                    dictionary_fra[word] += 1
                else:
                    dictionary_fra[word] = 1
        print "corpus added in french dictionary"

#this method validates the performance of the naive bayes classifier on the test corpus
def evaluate_model(test_corpus):

    test_corpus_r = []
    for word in test_corpus:
        if(word != ''):
            test_corpus_r.append(word)
    
    #print(test_corpus_r)
    
    for word in test_corpus_r:
        if (word in dictionary_test):
            dictionary_test[word] += 1
        else:
            dictionary_test[word] = 1
    print "count words in test document: %d"% len(test_corpus_r)
    
    #initializing initial probabilities to 1
    prob_eng = 1
    prob_deu = 1
    prob_fra = 1

    #total count of words in dictionaries
    countOfWord_eng = 0
    countOfWord_deu = 0
    countOfWord_fra = 0

    for key in dictionary_eng:
        countOfWord_eng += dictionary_eng[key]
    print "number of words in english dictionary is %d" %countOfWord_eng

    for key in dictionary_deu:
        countOfWord_deu += dictionary_deu[key]
    print "number of words in german dictionary is %d" %countOfWord_deu

    for key in dictionary_fra:
        countOfWord_fra += dictionary_fra[key]    
    print "number of words in french dictionary is %d" %countOfWord_fra

    for word in test_corpus_r:
        #print "word is %s" %word
        if word in dictionary_eng:
            #prob_eng = float(prob_eng * (dictionary_eng[word]+1))/(countOfWord_eng + len(dictionary_test))
            prob_eng = Decimal(prob_eng * (dictionary_eng[word]+1)) / Decimal(countOfWord_eng + len(test_corpus_r))
            #print(prob_eng)
            #print "is the value of prob of word %s in english, count is %d" %(word, dictionary_eng[word])
        else:
            #prob_eng = float(prob_eng * 1)/(countOfWord_eng + len(dictionary_test))
            prob_eng = Decimal(prob_eng * 1) / Decimal(countOfWord_eng + len(test_corpus_r))
            #print(prob_eng)
            #print "%s is not found in english" %word

    for word in test_corpus_r:
        #print "word is %s" %word
        if word in dictionary_deu:
            #prob_deu = float(prob_deu * (dictionary_deu[word]+1))/(countOfWord_deu + len(dictionary_test))
            prob_deu = Decimal(prob_deu * (dictionary_deu[word]+1)) / Decimal(countOfWord_deu + len(test_corpus_r))
            #print(prob_deu)
            #print "is the value of prob of word %s in german, count is %d" %(word, dictionary_deu[word])
        else:
            #prob_deu = float(prob_deu * 1)/(countOfWord_deu + len(dictionary_test))
            prob_deu = Decimal(prob_deu * 1) / Decimal(countOfWord_deu + len(test_corpus_r))
            #print(prob_deu)
            #print "%s is not found in german" %word

    for word in test_corpus_r:
        #print "word is %s" %word
        if word in dictionary_fra:
            #prob_fra = float(prob_fra * (dictionary_fra[word]+1))/(countOfWord_fra + len(dictionary_test))
            prob_fra = Decimal(prob_fra * (dictionary_fra[word]+1)) / Decimal(countOfWord_fra + len(test_corpus_r))
            #print(prob_fra)
            #print "is the value of prob of word %s in french, count is %d" %(word, dictionary_fra[word])
        else:
            #prob_fra = float(prob_fra * 1)/(countOfWord_fra + len(dictionary_test))
            prob_fra = Decimal(prob_fra * 1) / Decimal(countOfWord_fra + len(test_corpus_r))
            #print(prob_fra)
            #print "%s is not found in french" %word
    
    print "probability score of eng, german and french"
    print(prob_eng)
    print(prob_deu)
    print(prob_fra)
    
    print "normalised probability of eng, german and french"
    print(Decimal(prob_eng) / Decimal(prob_eng + prob_deu + prob_fra))
    print(Decimal(prob_deu) / Decimal(prob_eng + prob_deu + prob_fra))
    print(Decimal(prob_fra) / Decimal(prob_eng + prob_deu + prob_fra))

#execution starts here

#there should be two command line inputs: first one is a text file wherein absolute path
#of the corpus along with its language label (separated by space) is present. second one
# is the absolute path name of the test corpus
print "the two args are %s and %s"%(sys.argv[1], sys.argv[2])

#opening the text file containing the list of corpus path and corpus label
f1 = open(str(sys.argv[1]), 'r')

for line in f1:
    line_cnt = re.split('\s', line)

    filename = str(line_cnt[0])
    doc_class = str(line_cnt[1])

    print "path of corpus and corpus label is %s and %s respectively"%(filename, doc_class)

    #merging all lines of the corpus into a single string
    try:
        data = open(filename,"r").read().replace('\n', ' ')
    except UnicodeDecodeError:
        print("exception")
    data = data.lower()

    #splitting the corpus at each of the below mentioned characters
    a = re.split('\s|[.,"]|[0-9]', data)

    #constructing the dictionary from the corpus
    construct_dictionary(a, doc_class)
    print "addition of corpora complete"

#constructing test corpus
try:
    text = open(str(sys.argv[2]) ,"r").read().replace('\n', ' ')
except UnicodeDecodeError:
    print("Exception")
text = text.lower()

#splitting the corpus at each of the below mentioned characters
b = re.split('\s|[.,"]|[0-9]', text)

evaluate_model(b)
