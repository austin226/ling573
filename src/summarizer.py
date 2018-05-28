#!/usr/bin/python3

import os
import subprocess

class Summarizer:
    '''
    Given an array of sentences, will return an array of sentences
    that forms a summary.
    '''

    def __init__(self, coreference_resolver, segmenter, content_selector, info_order, sentence_realizer):
        self.coreference_resolver = coreference_resolver
        self.segmenter = segmenter
        self.content_selector = content_selector
        self.info_order = info_order
        self.sentence_realizer = sentence_realizer

    def _build_cluster(self, topic_id, docset):
        """Create a MEAD cluster file at 'var/docs/{topic_id}/{topic_id}.cluster'"""
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        init_dir = os.getcwd()
        os.chdir('{}/var/docs'.format(base_dir))

        topic_dir = topic_id
        os.makedirs(topic_dir, exist_ok=True)
        for doc_id, doc_info in docset.items():
            output_filename = '{}/{}'.format(topic_dir, doc_id)
            text = ' '.join(doc_info['paragraphs'])
            sentences = self.coreference_resolver.resolve(text)
            print("{} / {}: Resolved {} sentences.".format(topic_id, doc_id, len(sentences)))
            # Segement the sentences further as necessary
            segments = []
            for s in sentences:
                segments.extend(self.segmenter.process(s))
            print("{} / {}: Segemented into {} sentences.".format(topic_id, doc_id, len(segments)))

            # Trim the sentences using the sentence_realizer
            segments = self.sentence_realizer.process(segments)

            with open(output_filename, 'w', encoding='utf8') as f:
                for p in segments:
                    f.write(p + '\n')

        # Convert sentences to docsent files using text2cluster.pl
        export_lib = 'export PERL5LIB=/mnt/dropbox/17-18/573/code/mead/bin/addons/formatting/'
        perl_script = '/mnt/dropbox/17-18/573/code/mead/bin/addons/formatting/text2cluster.pl'
        command = '{} && {} {}'.format(export_lib, perl_script, topic_dir)
        # TODO use a more secure method than getoutput
        perl_output = subprocess.getoutput(command)

        os.chdir(init_dir)

    def summarize(self, topic_id, docset):
        if len(docset) == 0:
            return []

        self._build_cluster(topic_id, docset)

        doc_id_list, sent_idx_list, sentences, simplified_sentences  = self.content_selector.select(topic_id)
        print("{}: Selected {} sentences.".format(topic_id, len(sentences)))
        ordered_sentences = self.info_order.process(doc_id_list, sent_idx_list, sentences)
        realized_sentences = self.sentence_realizer.process(ordered_sentences, simplified_sentences)
        return realized_sentences
