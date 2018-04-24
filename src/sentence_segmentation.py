#!/usr/bin/python3

import nltk

from nltk.tokenize import sent_tokenize

nltk.data.path.append('/dropbox/17-18/573/code/cnn-dm-tools/brown/') # Import punkt corpus

class SentenceSegmenter:
    """A method for converting a block of text into a list of sentences using NLTK """

    def process(self, data):
        """Input is a block of text, and output is a list of sentences."""

        sent_list = sent_tokenize(data)

        return sent_list
