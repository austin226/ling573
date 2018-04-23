#!/usr/bin/python3

import subprocess
import sys

class SentenceExtractor:
    """The Extractor uses MEAD to examine a cluster and find the list of X (=max) best sentences."""


# Calls upon MEAD to pick the X best sentences (max = X) in cluster Y. Returns sentences in list form.

    def process(self, cluster, max):
        perl_script = "/mnt/dropbox/17-18/573/code/mead/bin/mead.pl"
        perl_output = subprocess.Popen([perl_script, "-a", "{0}".format(max), cluster], stdout=sys.stdout)
        perl_output.communicate()
        #TODO Capture output of Perl script
        #TODO Parse output and capture sentences.
        #    Format of output is [1] text \n
        #                        [2] text \n ... etc

# For testing purposes, instantiate an extractor and run on the default cluster (called GA3) available in the mead/data directory.
#        
# extractor = SentenceExtractor()
#
# extractor.process("GA3", 5)
