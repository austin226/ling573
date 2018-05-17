#!/usr/bin/python3

# Based on https://nlpforhackers.io/wordnet-sentence-similarity/

import fileinput
import nltk
import re
import sys

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

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

    def penn_to_wn(self, tag):
        """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
        if tag.startswith('N'):
            return 'n'

        if tag.startswith('V'):
            return 'v'

        if tag.startswith('J'):
            return 'a'

        if tag.startswith('R'):
            return 'r'

        return None

    def tagged_to_synset(self, word, tag, synset_cache):
        if (word, tag) in synset_cache:
            return synset_cache[(word, tag)]

        wn_tag = self.penn_to_wn(tag)
        if wn_tag is None:
            synset = None
        else:
            synsets = wn.synsets(word, wn_tag)
            if len(synsets) > 0:
                synset = synsets[0]
            else:
                synset = None
        synset_cache[(word, tag)] = synset
        return synset

    def sentence_similarity(self, sentence1, sentence2, sim_cache, synset_cache):
        """ compute the sentence similarity using Wordnet """
        if sentence1 not in sim_cache:
            sim_cache[sentence1] = {}
        elif sentence2 in sim_cache[sentence1]:
            return sim_cache[sentence1][sentence2]

        # Tokenize and tag
        s1_tokens = pos_tag(word_tokenize(sentence1))
        s2_tokens = pos_tag(word_tokenize(sentence2))

        # Get the synsets for the tagged words
        synsets1 = []
        synsets2 = []
        for word, tag in pos_tag(word_tokenize(sentence1)):
            synsets1.append(self.tagged_to_synset(word, tag, synset_cache))
        for word, tag in pos_tag(word_tokenize(sentence2)):
            synsets2.append(self.tagged_to_synset(word, tag, synset_cache))

        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]

        score, count = 0.0, 0

        # For each word in the first sentence
        for synset in synsets1:
            # Get the similarity value of the most similar word in the other sentence
            similarity_scores = []
            for ss in synsets2:
                similarity = synset.path_similarity(ss)
                if similarity is not None:
                    similarity_scores.append(similarity)
            if len(similarity_scores) == 0:
                continue
            score += max(similarity_scores)
            count += 1

        # Average the values
        if count != 0:
            score /= count
        else:
            score = 0

        sim_cache[sentence1][sentence2] = score
        return score

    #Balance out the differences in comparing A,B vs B,A
    def symmetric_sentence_similarity(self, sentence1, sentence2, sim_cache, synset_cache):
        """ compute the symmetric sentence similarity using Wordnet """
        return self.sentence_similarity(sentence1, sentence2, sim_cache, synset_cache) + self.sentence_similarity(sentence2, sentence1, sim_cache, synset_cache)

    #Find the two most similar sentences
    def initial_compare(self, sentences, sim_cache, synset_cache):
        max_similarity = -1
        pair = list()
        for s1 in range(0, len(sentences)):
            for s2 in range(s1+1, len(sentences)):
                similarity = self.symmetric_sentence_similarity(sentences[s1], sentences[s2], sim_cache, synset_cache)
                if similarity > max_similarity:
                    max_similarity = similarity
                    pair = [sentences[s1], sentences[s2]]
        return pair


    def process(self, doc_id_list, sent_idx_list, sentences):
        '''
        doc_id_list: format is like "XIN_ENG_20050210.0029" or "NYT19990424.0231"
        sentences: list of string sentences.

        doc_id_list[i] is the doc_id containing sentences[i]
        '''
      
        if len(sentences) == 0:
            return sentences

        sentencesList = list()
        sentencesOutput = list()
        chronologicalOrderedSentences = list()

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
            chronologicalOrderedSentences.append(sentence[1])

        #Find the 2 closest sentences
        sim_cache = {}
        synset_cache = {}
        similarityOrderedSentences = self.initial_compare(chronologicalOrderedSentences, sim_cache, synset_cache)
        chronologicalOrderedSentences.remove(similarityOrderedSentences[0])
        chronologicalOrderedSentences.remove(similarityOrderedSentences[1])
        #Check both sides of the list of processed sentences to find the closest match
        while len(chronologicalOrderedSentences) > 0:
            max_similarity = -1
            for s in chronologicalOrderedSentences:
                similarity = self.symmetric_sentence_similarity(similarityOrderedSentences[0], s, sim_cache, synset_cache)
                if similarity > max_similarity:
                    max_similarity = similarity
                    candidate = [0, s]
            for s in chronologicalOrderedSentences:
                similarity = self.symmetric_sentence_similarity(similarityOrderedSentences[-1], s, sim_cache, synset_cache)
                if similarity > max_similarity:
                    max_similarity = similarity
                    candidate = [len(chronologicalOrderedSentences), s]

            if not candidate:
                continue
            #add the sentence to similarity ordered, remove from chronologically ordered
            chronologicalOrderedSentences.remove(candidate[1])
            similarityOrderedSentences.insert(candidate[0], candidate[1])
            
        return similarityOrderedSentences

    def to_numeric_list(self, doc_id_list):
        '''
        Convert a list of doc_ids to numeric strings
        '''
        return [re.sub('[^0-9]', '', doc_id) for doc_id in doc_id_list]
