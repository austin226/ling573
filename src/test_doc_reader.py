#!/usr/bin/python3

import os
import unittest

from doc_reader import DocReader

class DocReaderTest(unittest.TestCase):
    def setUp(self):
        self.aq_root = '/dropbox/17-18/573/AQUAINT'
        self.aq2_root = '/dropbox/17-18/573/AQUAINT-2'
        self.doc_reader = DocReader(self.aq_root, self.aq2_root)

    def test_resolve_path(self):
        test_data = [
            ('XIE19990529.0166', (self.aq_root+'/xie/1999/19990529_XIN_ENG', 'AQUAINT')),
            ('APW19990421.0284', (self.aq_root+'/apw/1999/19990421_APW_ENG', 'AQUAINT')),
            ('NYT19990421.0284', (self.aq_root+'/nyt/1999/19990421_NYT', 'AQUAINT')),
            ('XIN_ENG_20050415.0040 ', (self.aq2_root+'/data/xin_eng/xin_eng_200504.xml', 'AQUAINT-2')),
        ]
        for doc_id, path in test_data:
            with self.subTest():
                self.assertEqual(path, self.doc_reader.resolve_path(doc_id))

        # Test invalid doc_id
        with self.assertRaises(ValueError) as cm:
            self.doc_reader.resolve_path('foo')

    def test_parse_doc(self):
        test_data = [
            ('/corpora/LDC/LDC02T31/apw/1998/19980601_APW_ENG', 'AQUAINT', 'APW19980601.0007'),
            ('/corpora/LDC/LDC08T25/data/apw_eng/apw_eng_200601.xml', 'AQUAINT-2', 'APW_ENG_20060101.0027'),
        ]
        for path, format_name, doc_id in test_data:
            content = self.doc_reader.parse_doc(path, format_name, doc_id)
            print(content)

    def test_read(self):
        #input_xml_filename = '/dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml'
        test_data_dir = os.path.dirname(os.path.realpath(__file__)) + '/test_data'
        input_xml_filename = test_data_dir + '/test_topics.xml'
        topics_data = self.doc_reader.read_docs(input_xml_filename)
        print(topics_data)

if __name__ == '__main__':
    unittest.main()
