#!/usr/bin/python3

import unittest

from sentence_extraction import SentenceExtractor

class SentenceExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor = SentenceExtractor(5)

    def testDocIDs(self):
        extract = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE EXTRACT SYSTEM "/clair/tools/mead/dtd/extract.dtd">

<EXTRACT QID="D1003A" LANG="ENG" COMPRESSION="5" SYSTEM="MEADORIG" RUN="Mon Apr 23 18:54:01 2018">
<S ORDER="1" DID="AFP_ENG_20050128.0218" SNO="1" />
<S ORDER="2" DID="AFP_ENG_20050128.0218" SNO="3" />
<S ORDER="3" DID="XIN_ENG_20041019.0235" SNO="1" />
<S ORDER="4" DID="XIN_ENG_20050210.0029" SNO="1" />
<S ORDER="5" DID="XIN_ENG_20050210.0029" SNO="2" />
</EXTRACT>
'''
        doc_ids = self.extractor.parse_doc_id_list(extract)
        print(doc_ids)

    def testExtractor(self):
        # For testing purposes, instantiate an extractor and run
        # on the default cluster (called GA3) available in the mead/data directory.
        cluster = 'GA3'
        doc_id_list, sentences = self.extractor.process(cluster)
        print(doc_id_list, sentences)
        self.assertTrue(len(sentences) == 5)

if __name__ == '__main__':
    unittest.main()
