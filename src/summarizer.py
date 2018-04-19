#!/usr/bin/python3

class Summarizer:
    '''
    Given an array of sentences, will return an array of sentences
    that forms a summary.
    '''

    def __init__(self, content_selector, info_order, sentence_realizer):
        self.content_selector = content_selector
        self.info_order = info_order
        self.sentence_realizer = sentence_realizer

    def summarize(self, sentences):
        selected_sentences = self.content_selector.select(sentences)
        ordered_sentences = self.info_order.process(selected_sentences)
        realized_sentences = self.sentence_realizer.process(sentences)
        return realized_sentences
