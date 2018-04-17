#!/usr/bin/python3

import unittest
from content_selection import ContentSelector
from sentence_extraction import SentenceExtractor
from sentence_simplification import SentenceSimplifier
from sentence_segmentation import SentenceSegmenter

class ContentSelectorTest(unittest.TestCase):
    def setUp(self):
        extractor = SentenceExtractor()
        simplifier = SentenceSimplifier()
        segmenter = SentenceSegmenter()

        self.content_selector = ContentSelector(extractor, simplifier, segmenter)

    def test_basic_order(self):
        sentences = [
                'This is the first sentence.',
                'This is the second sentence.',
        ]
        processed = self.content_selector.select(sentences)

        self.assertEqual(sentences, processed)

if __name__ == '__main__':
    unittest.main()
