#!/usr/bin/python3

import unittest
from content_selection import ContentSelector
from sentence_extraction import SentenceExtractor
from sentence_simplification import SentenceSimplifier
from sentence_segmentation import SentenceSegmenter

class ContentSelectorTest(unittest.TestCase):
    def setUp(self):
        extractor = SentenceExtractor(5)
        simplifier = SentenceSimplifier()
        segmenter = SentenceSegmenter()

        self.content_selector = ContentSelector(extractor, simplifier, segmenter)

    def test_dummy(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()
