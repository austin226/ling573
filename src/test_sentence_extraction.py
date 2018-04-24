#!/usr/bin/python3

import unittest

from sentence_extraction import SentenceExtractor

class SentenceExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor = SentenceExtractor()

    def testExtractor(self):
        # For testing purposes, instantiate an extractor and run
        # on the default cluster (called GA3) available in the mead/data directory.
        cluster = 'GA3'
        max_sent = 5
        output = self.extractor.process(cluster, max_sent)
        print(output)
        self.assertTrue(len(output) == 5)

if __name__ == '__main__':
    unittest.main()
