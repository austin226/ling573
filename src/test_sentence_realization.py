#!/usr/bin/python3

import unittest
from sentence_realization import SentenceRealizer

class SentenceRealizerTest(unittest.TestCase):
    def setUp(self):
        self.sr = SentenceRealizer()

    def test_basic_order(self):
        sentences = [
                'This is the first sentence.',
                'This is the second sentence.',
        ]
        processed = self.sr.process(sentences)

        self.assertEqual(sentences, processed)

if __name__ == '__main__':
    unittest.main()
