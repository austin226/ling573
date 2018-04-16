#!/usr/bin/python3

import unittest
from sentence_realization import SentenceRealizer

class SentenceRealizerTest(unittest.TestCase):
    def test_dummy(self):
        sentence_realizer = SentenceRealizer()
        sentence_realizer.process(['sent1', 'sent2'])
        print('ok')

if __name__ == '__main__':
    unittest.main()
