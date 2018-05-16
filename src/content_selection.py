#!/usr/bin/python3

class ContentSelector:
    '''
    This class will identify the most prominent sentences from among
    those presented.
    '''

    def __init__(self, extractor, simplifier):
        self.extractor = extractor
        self.simplifier = simplifier

    def select(self, topic_id):
        # doc_id_list, sent_idx_list, and extracted should all be the same length
        doc_id_list, sent_idx_list, extracted = self.extractor.process(topic_id)

        # Repeat entries in doc_id_list and sent_idx_list whenever a block is split

        sentences = [] # Segmented list of sentences
        doc_id_list_seg = [] # Doc ID of each sentence
        sent_idx_list_seg = [] # Index within doc for each sentence
        for i, sentence in enumerate(extracted):
            doc_id = doc_id_list[i]
            sent_idx = sent_idx_list[i]
            sentences.append(sentence)
            doc_id_list_seg.append(doc_id)
            sent_idx_list_seg.append(sent_idx)

        sentences_simp = [self.simplifier.process(s) for s in sentences]

        return doc_id_list_seg, sent_idx_list_seg, sentences, sentences_simp
