#!/usr/bin/python3

import os
import subprocess

class Summarizer:
    '''
    Given an array of sentences, will return an array of sentences
    that forms a summary.
    '''

    def __init__(self, content_selector, info_order, sentence_realizer):
        self.content_selector = content_selector
        self.info_order = info_order
        self.sentence_realizer = sentence_realizer

    def _build_cluster(self, topic_id, docset):
        """Create a MEAD cluster file at 'var/docs/{topic_id}/{topic_id}.cluster'"""
        init_dir = os.getcwd()
        os.chdir('var/docs')

        topic_dir = topic_id
        os.makedirs(topic_dir, exist_ok=True)
        for doc_id, doc_info in docset.items():
            output_filename = '{}/{}'.format(topic_dir, doc_id)
            paragraphs = doc_info['paragraphs']
            with open(output_filename, 'w') as f:
                for p in paragraphs:
                    f.write(p + '\n')

        # Convert sentences to docsent files using text2cluster.pl
        export_lib = 'export PERL5LIB=/mnt/dropbox/17-18/573/code/mead/bin/addons/formatting/'
        perl_script = '/mnt/dropbox/17-18/573/code/mead/bin/addons/formatting/text2cluster.pl'
        command = '{} && {} {}'.format(export_lib, perl_script, topic_dir)
        # TODO use a more secure method than getoutput
        perl_output = subprocess.getoutput(command)

        os.chdir(init_dir)

    def summarize(self, topic_id, docset):
        self._build_cluster(topic_id, docset)

        doc_id_list, selected_sentences = self.content_selector.select(topic_id)
        ordered_sentences = self.info_order.process(doc_id_list, selected_sentences)
        #realized_sentences = self.sentence_realizer.process(sentences)
        #return realized_sentences
