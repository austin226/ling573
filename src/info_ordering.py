#!/usr/bin/python3

import fileinput
import re
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

    def process(self, doc_id_list, sent_idx_list, sentences):
        '''
        doc_id_list: format is like "XIN_ENG_20050210.0029" or "NYT19990424.0231"
        sentences: list of string sentences.

        doc_id_list[i] is the doc_id containing sentences[i]
        '''
      
        sentencesList = list()
        sentencesOutput = list()

        numeric_date_list = self.to_numeric_list(doc_id_list)
        
        #Add sentences to the list
        for i, line in enumerate(sentences):
            date_num_str = numeric_date_list[i]
            # Format idx as a 4-digit numeric string
            sent_idx = '{:0>4d}'.format(sent_idx_list[i])
            dateSeq = date_num_str + sent_idx
            sentencesList.append((dateSeq,line))

        #sort the setences according to the date and sequence
        sentencesList.sort(key=lambda tup: tup[0])

        for sentence in sentencesList:
            sentencesOutput.append(sentence[1])
            
        return sentencesOutput

    def to_numeric_list(self, doc_id_list):
        '''
        Convert a list of doc_ids to numeric strings
        '''
        return [re.sub('[^0-9]', '', doc_id) for doc_id in doc_id_list]
