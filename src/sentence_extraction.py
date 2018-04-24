#!/usr/bin/python3

import os
import subprocess
import sys

class SentenceExtractor:
    """The Extractor uses MEAD to examine a cluster and find the list of X (=max_sent) best sentences."""
    def __init__(self, max_sent):
        """max_sent = max sentences per cluster to select"""
        self.max_sent = max_sent

    def process(self, cluster):
        """Calls upon MEAD to pick the X best sentences (max_sent = X) in cluster Y. Returns sentences in list form."""
        perl_script = "/mnt/dropbox/17-18/573/code/mead/bin/mead.pl"
        rc_filename = os.path.dirname(os.path.realpath(__file__)) + '/.meadrc'
        command = '{} -rc {} -a {} {} 2>/dev/null'.format(perl_script, rc_filename, self.max_sent, cluster)
        # TODO use a more secure method than getoutput
        perl_output = subprocess.getoutput(command)
        sentences = self.parse_sentences(perl_output)
        return sentences

    def parse_sentences(self, perl_output):
        """
        Parse output and capture sentences.
            Format of output is [1] text \n
                                [2] text \n ... etc
        """
        lines = [line.strip().split(' ', 1)[1].strip() for line in perl_output.split('\n')]
        return lines
