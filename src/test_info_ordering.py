#!/usr/bin/python3

import unittest
from info_ordering import InfoOrder

class InfoOrderTest(unittest.TestCase):
    def setUp(self):
        self.info_ord = InfoOrder()

    def test_to_numeric_list(self):
        doc_id_list = ['NYT19990424.0231','XIN_ENG_20050210.0029']
        numeric_list = ['199904240231', '200502100029']
        self.assertEqual(numeric_list, self.info_ord.to_numeric_list(doc_id_list))

    def test_basic_order(self):
        doc_id_list = ['XIN_ENG_20050210.0029','NYT19990424.0231']
        sentences = [
            'This is the second sentence.',
            'This is the first sentence.',
        ]
        processed = self.info_ord.process(doc_id_list, sentences)

        self.assertEqual([sentences[1], sentences[0]], processed)

if __name__ == '__main__':
    unittest.main()
