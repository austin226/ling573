#!/usr/bin/python3

class ContentSelector:
    '''
    This class will identify the most prominent sentences from among
    those presented.
    '''

    def __init__(self, extractor, simplifier, segmenter):
        self.extractor = extractor
        self.simplifier = simplifier
        self.segmenter = segmenter

    def select(self, sentences):
        extracted = self.extractor.process(sentences)
        simplified = self.simplifier.process(extracted)
        segmented = self.segmenter.process(simplified)
        return segmented
