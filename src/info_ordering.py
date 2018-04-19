#!/usr/bin/python3
import fileinput
import sys


#input object is expected to have the following for each line:
#date sequence 'sentence' with date formatted as YYYYMMDDHHSS; sequence represents intra-document sentence ordering
#when one document has multiple sentences. sentence represents the actual sentence

#output file format is the following for each line:
# sentence


class InfoOrder:
    '''
    This class will accept a set of sentences, and return them in a
    logical order. (e.g., chronological or by importance)
    '''

    def process(self, sentences):
      
        sentencesList = list()
        sentencesOutput = list()
        
        #Add sentences to the list
        for line in sentences:
            items = line.split('#')
            dateSeq = items[0] + items[1]
            sentencesList.append((dateSeq,items[2]))


        #sort the setences according to the date and sequence
        sentencesList.sort(key=lambda tup: tup[0])

        for sentence in sentencesList:
            sentencesOutput.append(sentence)
            
        return sentencesOutput