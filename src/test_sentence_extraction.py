#!/usr/bin/python3

import unittest

from sentence_extraction import SentenceExtractor

class SentenceExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor = SentenceExtractor(5)

    def testExtractor(self):
        # For testing purposes, instantiate an extractor and run
        # on the default cluster (called GA3) available in the mead/data directory.
        cluster = 'GA3'
        doc_id_list, sentences = self.extractor.process(cluster)
        print(doc_id_list, sentences)
        self.assertTrue(len(sentences) == 5)

if __name__ == '__main__':
    unittest.main()
