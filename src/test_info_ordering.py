#!/usr/bin/python3

import unittest
from info_ordering import InfoOrder

class InfoOrderTest(unittest.TestCase):
    def setUp(self):
        self.info_ord = InfoOrder()

    def test_basic_order(self):
        sentences = [
                'This is the first sentence.',
                'This is the second sentence.',
        ]
        processed = self.info_ord.process(sentences)

        self.assertEqual(sentences, processed)

if __name__ == '__main__':
    unittest.main()
