#!/usr/bin/python3

import unittest
from content_selection import ContentSelector

class ContentSelectorTest(unittest.TestCase):
    def setUp(self):
        self.content_selector = ContentSelector()

    def test_basic_order(self):
        sentences = [
                'This is the first sentence.',
                'This is the second sentence.',
        ]
        processed = self.content_selector.select(sentences)

        self.assertEqual(sentences, processed)

if __name__ == '__main__':
    unittest.main()
