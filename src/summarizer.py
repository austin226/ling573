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

    def summarize(self, docset):
        output_dir = 'var/docs/'
        for doc_id, doc_info in docset.items():
            output_filename = 'var/docs/{}'.format(doc_id)
            paragraphs = doc_info['paragraphs']
            with open(output_filename, 'w') as f:
                for p in paragraphs:
                    f.write(p + '\n')

        selected_sentences = self.content_selector.select(sentences)
        ordered_sentences = self.info_order.process(selected_sentences)
        realized_sentences = self.sentence_realizer.process(sentences)
        return realized_sentences
