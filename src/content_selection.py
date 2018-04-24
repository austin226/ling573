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

    def select(self, topic_id):
        extracted = self.extractor.process(topic_id)
        simplified = [self.simplifier.process(e) for e in extracted]
        segmented = [self.segmenter.process(s) for s in simplified]

        sentences = []
        for s in simplified:
            sentences.extend(self.segmenter.process(s))
        return sentences
