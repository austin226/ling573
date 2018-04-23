#!/usr/bin/python3

from nltk.tokenize import sent_tokenize

class SentenceSegmenter:
    """A method for converting a block of text into a list of sentences using NLTK """

    def process(self, data):
        """Input is a block of text, and output is a list of sentences."""

        sent_list = sent_tokenize(data)

        return sent_list
