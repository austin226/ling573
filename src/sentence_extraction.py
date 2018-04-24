#!/usr/bin/python3

import os
import subprocess
import sys

class SentenceExtractor:
    """The Extractor uses MEAD to examine a cluster and find the list of X (=max_sent) best sentences."""

# Calls upon MEAD to pick the X best sentences (max_sent = X) in cluster Y. Returns sentences in list form.

    def process(self, cluster, max_sent):
        perl_script = "/mnt/dropbox/17-18/573/code/mead/bin/mead.pl"
        rc_filename = os.path.dirname(os.path.realpath(__file__)) + '/.meadrc'
        command = '{} -rc {} -a {} {} 2>/dev/null'.format(perl_script, rc_filename, max_sent, cluster)
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
