'''
Created on 19-Aug-2015

Description: automatic text based language classification system for 3 Latin languages using naive bayes

@author: biswajeet
'''

import re
import sys
from decimal import *

getcontext().prec = 20  #precesion of the probabilities

#unigram dictionaries
dictionary_eng = {}
dictionary_deu = {}
dictionary_fra = {}

dictionary_test = {}

#bigram dictionaries
bi_dictionary_eng = {}
bi_dictionary_deu = {}
bi_dictionary_fra = {}

bi_dictionary_test = {}

#this method constructs/updates dictionary based on the corpus label
def construct_dictionary(array, doc_class):
    doc = str(doc_class) #corpus label
    
    #construct unigram and bigram english dict
    if (doc == 'eng'):
        preword = ''

        for word in array:
            if (word in dictionary_eng):
                dictionary_eng[word] += 1
            else:
                dictionary_eng[word] = 1

            #if 'word' is not the first word then we start construct the bigram
            if preword != '':
                if not bi_dictionary_eng.has_key(preword):
                    bi_dictionary_eng[preword] = {}
                    bi_dictionary_eng[preword][word] = 1
                else:
                    if not bi_dictionary_eng[preword].has_key(word):
                        bi_dictionary_eng[preword][word] = 1
                    else:
                        bi_dictionary_eng[preword][word] += 1
            preword = word
        print "corpus added in english unigram and bigram dictionary"

    #construct unigram and bigram german dict
    if (doc == 'deu'):
        preword = ''

        for word in array:
            if (word in dictionary_deu):
                dictionary_deu[word] += 1
            else:
                dictionary_deu[word] = 1

            #if 'word' is not the first word then we start construct the bigram
            if preword != '':
                if not bi_dictionary_deu.has_key(preword):
                    bi_dictionary_deu[preword] = {}
                    bi_dictionary_deu[preword][word] = 1
                else:
                    if not bi_dictionary_deu[preword].has_key(word):
                        bi_dictionary_deu[preword][word] = 1
                    else:
                        bi_dictionary_deu[preword][word] += 1
            preword = word
        print "corpus added in german unigram and bigram dictionary"

    #construct unigram and bigram french dict
    if (doc == 'fra'):
        preword = ''

        for word in array:
            if (word in dictionary_fra):
                dictionary_fra[word] += 1
            else:
                dictionary_fra[word] = 1

            #if 'word' is not the first word then we start construct the bigram
            if preword != '':
                if not bi_dictionary_fra.has_key(preword):
                    bi_dictionary_fra[preword] = {}
                    bi_dictionary_fra[preword][word] = 1
                else:
                    if not bi_dictionary_fra[preword].has_key(word):
                        bi_dictionary_fra[preword][word] = 1
                    else:
                        bi_dictionary_fra[preword][word] += 1
            preword = word
        print "corpus added in french unigram and bigram dictionary"

#this method validates the performance of the naive bayes classifier on the test corpus
def evaluate_model(test_corpus):

    print "count words in test document: %d"% len(test_corpus)
    
    #initializing initial probabilities to 1
    prob = [1,1,1]

    uni_prob = [1,1,1]
    bi_prob = [1,1,1]

    #total count of words in dictionaries

    bi_countOfWord = [0, 0, 0]

    for key in bi_dictionary_eng:
        bi_countOfWord[0] += sum(bi_dictionary_eng[key].values())
    #print "number of words in english dictionary is %d" %bi_countOfWord[0]

    for key in bi_dictionary_deu:
        bi_countOfWord[1] += sum(bi_dictionary_deu[key].values())
    #print "number of words in german dictionary is %d" %bi_countOfWord[1]

    for key in dictionary_fra:
        bi_countOfWord[2] += sum(bi_dictionary_fra[key].values())
    #print "number of words in french dictionary is %d" %bi_countOfWord[2]
    #------------------------------------------------
    countOfWord = [sum(dictionary_eng.values()), sum(dictionary_deu.values()), sum(dictionary_fra.values())]

    print "# words in english dictionary ", countOfWord[0], len(dictionary_eng.keys())

    print "# words in german dictionary ", countOfWord[1], len(dictionary_deu.keys())

    print "# words in french dictionary ", countOfWord[2], len(dictionary_fra.keys())

    preword = ''
    for word in test_corpus:
        #print "word is %s" %word
        if word in dictionary_eng:
            #prob_eng = float(prob_eng * (dictionary_eng[word]+1))/(countOfWord_eng + len(dictionary_test))
            uni_prob[0] = Decimal(uni_prob[0] * (dictionary_eng[word]+1)) / Decimal(countOfWord[0] + len(test_corpus))
            #print(prob_eng)
            #print "is the value of prob of word %s in english, count is %d" %(word, dictionary_eng[word])
        else:
            #prob_eng = float(prob_eng * 1)/(countOfWord_eng + len(dictionary_test))
            uni_prob[0] = Decimal(uni_prob[0] * 1) / Decimal(countOfWord[0] + len(test_corpus))
            #print(prob_eng)
            #print "%s is not found in english" %word

        #--------german dictionary-----------------------------------------------------------------
        if word in dictionary_deu:
            #prob_eng = float(prob_eng * (dictionary_eng[word]+1))/(countOfWord_eng + len(dictionary_test))
            uni_prob[1] = Decimal(uni_prob[1] * (dictionary_deu[word]+1)) / Decimal(countOfWord[1] + len(test_corpus))
            #print(prob_eng)
            #print "is the value of prob of word %s in english, count is %d" %(word, dictionary_eng[word])
        else:
            #prob_eng = float(prob_eng * 1)/(countOfWord_eng + len(dictionary_test))
            uni_prob[1] = Decimal(uni_prob[1] * 1) / Decimal(countOfWord[1] + len(test_corpus))
            #print(prob_eng)
            #print "%s is not found in english" %word

        #--------french dictionary-----------------------------------------------------------------
        if word in dictionary_fra:
            #prob_eng = float(prob_eng * (dictionary_eng[word]+1))/(countOfWord_eng + len(dictionary_test))
            uni_prob[2] = Decimal(uni_prob[2] * (dictionary_fra[word]+1)) / Decimal(countOfWord[2] + len(test_corpus))
            #print(prob_eng)
            #print "is the value of prob of word %s in english, count is %d" %(word, dictionary_eng[word])
        else:
            #prob_eng = float(prob_eng * 1)/(countOfWord_eng + len(dictionary_test))
            uni_prob[2] = Decimal(uni_prob[2] * 1) / Decimal(countOfWord[2] + len(test_corpus))
            #print(prob_eng)
            #print "%s is not found in english" %word

        if preword != '':
            if bi_dictionary_eng.has_key(preword) and bi_dictionary_eng[preword].has_key(word):
                bi_prob[0] = Decimal(bi_prob[0] * (bi_dictionary_eng[preword][word] + 1)) / \
                             Decimal(bi_countOfWord[0] + (len(test_corpus) - 1))
            else:
                bi_prob[0] = Decimal(bi_prob[0] * 1) / Decimal(bi_countOfWord[0] + (len(test_corpus) - 1))

            #-----german---------------------------------------------------------------------------------------
            if bi_dictionary_deu.has_key(preword) and bi_dictionary_deu[preword].has_key(word):
                bi_prob[1] = Decimal(bi_prob[1] * (bi_dictionary_deu[preword][word] + 1)) / \
                             Decimal(bi_countOfWord[1] + (len(test_corpus) - 1))
            else:
                bi_prob[1] = Decimal(bi_prob[1] * 1) / Decimal(bi_countOfWord[1] + (len(test_corpus) - 1))

            #-----french---------------------------------------------------------------------------------------
            if bi_dictionary_fra.has_key(preword) and bi_dictionary_fra[preword].has_key(word):
                bi_prob[2] = Decimal(bi_prob[2] * (bi_dictionary_fra[preword][word] + 1)) / \
                             Decimal(bi_countOfWord[2] + (len(test_corpus) - 1))
            else:
                bi_prob[2] = Decimal(bi_prob[2] * 1) / Decimal(bi_countOfWord[2] + (len(test_corpus) - 1))


        preword = str(word)

    prob[0] = Decimal(0.4)*uni_prob[0] + Decimal(0.6)*bi_prob[0]
    prob[1] = Decimal(0.4)*uni_prob[1] + Decimal(0.6)*bi_prob[1]
    prob[2] = Decimal(0.4)*uni_prob[2] + Decimal(0.6)*bi_prob[2]
    
    print "UNI-GRAM score"
    print(uni_prob[0], uni_prob[1], uni_prob[2])
    print "Bi-GRAM score"
    print(bi_prob[0], bi_prob[1], bi_prob[2])
    print "net score of eng, german and french"
    print(prob[0], prob[1], prob[2])
    
    print "UNI-GRAM probability"
    print(Decimal(uni_prob[0]) / Decimal(uni_prob[0] + uni_prob[1] + uni_prob[2]))
    print(Decimal(uni_prob[1]) / Decimal(uni_prob[0] + uni_prob[1] + uni_prob[2]))
    print(Decimal(uni_prob[2]) / Decimal(uni_prob[0] + uni_prob[1] + uni_prob[2]))

    print "Bi-GRAM probability "
    print(Decimal(bi_prob[0]) / Decimal(bi_prob[0] + bi_prob[1] + bi_prob[2]))
    print(Decimal(bi_prob[1]) / Decimal(bi_prob[0] + bi_prob[1] + bi_prob[2]))
    print(Decimal(bi_prob[2]) / Decimal(bi_prob[0] + bi_prob[1] + bi_prob[2]))

    print "net probability of eng, german and french"
    print(Decimal(prob[0]) / Decimal(prob[0] + prob[1] + prob[2]))
    print(Decimal(prob[1]) / Decimal(prob[0] + prob[1] + prob[2]))
    print(Decimal(prob[2]) / Decimal(prob[0] + prob[1] + prob[2]))

#execution starts here

#there should be 2 command line inputs: first arg is path of a text file wherein absolute path
#of the corpora along with their language label (separated by space) is present. Second one
# is the absolute path of the test corpus
print "the two args are %s and %s"%(sys.argv[1], sys.argv[2])

#open the text file containing the list of corpus path and corpus label
f1 = open(str(sys.argv[1]), 'r')

for line in f1:
    line_cnt = re.split('\s', line)

    filename = str(line_cnt[0])
    doc_class = str(line_cnt[1])

    print "path of corpus and corpus label is %s and %s respectively"%(filename, doc_class)

    #merge all lines of the corpus into a single string
    try:
        data = open(filename,"r").read().replace('\n', ' ')
    except UnicodeDecodeError:
        print("exception")
    #convert all letters to lowercase
    data = data.lower()

    #corpus is split at each of the following characters
    a = re.split('\s|[.,"]|[0-9]', data)

    #eliminate null characters
    a = [x for x in a if x != '']

    #constructing the dictionary from the corpus
    construct_dictionary(a, doc_class)
    print "addition of "+ doc_class +" corpora complete"

#constructing test corpus
try:
    text = open(str(sys.argv[2]) ,"r").read().replace('\n', ' ')
except UnicodeDecodeError:
    print("Exception")
text = text.lower()

#splitting the corpus at each specific characters
b = re.split('\s|[.,"]|[0-9]', text)
b = [x for x in b if x != '']

evaluate_model(b)
