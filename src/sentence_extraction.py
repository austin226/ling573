#!/usr/bin/python3

import os
import subprocess
import sys

from lxml import etree as ET

class SentenceExtractor:
    """The Extractor uses MEAD to examine a cluster and find the list of X (=max_sent) best sentences."""
    def __init__(self, max_sent):
        """max_sent = max sentences per cluster to select"""
        self.max_sent = max_sent

    def process(self, cluster):
        """Calls upon MEAD to pick the X best sentences (max_sent = X) in cluster Y. Returns sentences in list form."""
        perl_script = "/mnt/dropbox/17-18/573/code/mead/bin/mead.pl"
        rc_filename = os.path.dirname(os.path.realpath(__file__)) + '/.meadrc'

        # TODO use a more secure method than getoutput
        extract_command = '{} -extract -rc {} -a {} {} 2>/dev/null'.format(perl_script, rc_filename, self.max_sent, cluster)
        summary_command = '{} -rc {} -a {} {} 2>/dev/null'.format(perl_script, rc_filename, self.max_sent, cluster)

        extract = subprocess.getoutput(extract_command)
        doc_id_list, sent_idx_list = self.parse_doc_id_list(extract)

        summary = subprocess.getoutput(summary_command)
        sentences = self.parse_sentences(summary)
        return doc_id_list, sent_idx_list, sentences

    def parse_doc_id_list(self, extract):
        '''
        Returns (doc_id_list, sent_idx_list)
        where doc_id_list is an ordered list of document IDs (one per sentence),
        and sent_idx_list is each sentence's index within that document
        '''
        parser = ET.XMLParser(dtd_validation=False, encoding='utf-8')
        tree = ET.fromstring(extract.encode('utf-8'), parser)
        doc_id_list = []
        sent_idx_list = []

        for s in tree:
            doc_id_list.append(s.get('DID'))
            sent_idx_list.append(int(s.get('SNO')))
        return doc_id_list, sent_idx_list

    def parse_sentences(self, perl_output):
        """
        Parse output and capture sentences.
            Format of output is [1] text \n
                                [2] text \n ... etc
        """
        lines = [line.strip().split(' ', 1)[1].strip() for line in perl_output.split('\n')]
        return lines
