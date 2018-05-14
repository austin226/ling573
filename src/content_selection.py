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
        # doc_id_list, sent_idx_list, and extracted should all be the same length
        doc_id_list, sent_idx_list, extracted = self.extractor.process(topic_id)

        # Repeat entries in doc_id_list and sent_idx_list whenever a block is split

        sentences_seg = [] # Segmented list of sentences
        doc_id_list_seg = [] # Doc ID of each sentence
        sent_idx_list_seg = [] # Index within doc for each sentence
        for i, block in enumerate(extracted):
            doc_id = doc_id_list[i]
            sent_idx = sent_idx_list[i]
            segments = self.segmenter.process(block)
            for seg in segments:
                sentences_seg.append(seg)
                doc_id_list_seg.append(doc_id)
                sent_idx_list_seg.append(sent_idx)

        sentences_simp = [self.simplifier.process(s) for s in sentences_seg]

        return doc_id_list_seg, sent_idx_list_seg, sentences_seg, sentences_simp
