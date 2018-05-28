#!/usr/bin/python3

import nltk
import re

from nltk import word_tokenize

class SentenceRealizer:
    '''
    The goal of this class is to "create a fluent, readable, compact output",
    converting a set of sentences into a coherent narrative.
    '''

    def process(self, sentences, simplified=[]):
        '''
        Use both full and simplified format for each sentence to form a coherent list of sentences
        '''

        # Remove spaces before any non-word
        sentences = [self.compress_sentence(s) for s in sentences]
        return sentences

    def compress_sentence(self, sentence):
        # Use sentence trimming rules similar to CLASSY 2006
        # Conroy, John & Schlesinger, Judith & O'leary, Dianne & Stewart, Jade. (2018). Back to basics: Classy 2006.
        sentence = self.remove_extraneous_words(sentence)
        sentence = self.remove_extra_spaces(sentence)
        sentence = sentence.strip()
        if len(sentence) > 0:
            sentence = sentence[0].upper() + sentence[1:]
        return sentence

    def remove_extra_spaces(self, sentence):
        tokens = sentence.split(' ')
        output = []
        for t in tokens:
            if t[0].isalnum() or t == '--' or t == '_':
                output.append(t)
            elif not output:
                # No tokens in output yet
                output.append(t)
            else:
                # Token is not a word, append to last token in output
                output[-1] += t
        return ' '.join(output)

    def remove_extraneous_words(self, sentence):
        # Remove extraneous words that appear in a sentence, including date lines, editor's comments, and so on.
        tokens = word_tokenize(sentence)

        # Replace '_' tokens with '--'
        tokens = ['--' if t == '_' else t for t in tokens]

        tokens_pos = nltk.pos_tag(tokens)
        tokens_pos = self.remove_dateline(tokens_pos)

        tokens = [token_pos[0] for token_pos in tokens_pos]
        return ' '.join(tokens)

    def remove_dateline(self, tokens_pos):
        '''
        A dateline consists of 'NNP', 'CD', and ',' tokens followed by a ':' token
        If tokens_pos begins with such a sequence, remove that sequence
        '''
        for i, token_pos in enumerate(tokens_pos):
            token, pos = token_pos
            if pos not in ['NNP', 'CD', ',', ':']:
                # We have reached a non-dateline token before the ':' -- return input
                return tokens_pos
            if pos == ':':
                # Return all tokens after the ':' token
                return tokens_pos[i+1:]
        return tokens_pos
