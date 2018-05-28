#!/usr/bin/python3

import sys
import unittest
from collections import OrderedDict
from coreference import CoreferenceResolver

port = None

class CoreferenceResolverTest(unittest.TestCase):
    def setUp(self):
        self.coref = CoreferenceResolver(port)

    def testReplaceTokens(self):
        tokens = OrderedDict([(0, 'zero'), (1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')])

        tokens = self.coref.replace_tokens(tokens, 'foo', 1, 3)
        self.assertEqual(OrderedDict([(0, 'zero'), (1, 'foo'), (3, 'three'), (4, 'four')]), tokens)

        tokens = self.coref.replace_tokens(tokens, 'bar', 3, 5)
        self.assertEqual(OrderedDict([(0, 'zero'), (1, 'foo'), (3, 'bar')]), tokens)

    def testResolve(self):
        text = '''
        Bill Clinton was governor of his home state of Arkansas. From humble beginnings he rose to the highest office in the land. Clinton was involved in a private affair with someone he knew.
        '''

        expected = [
            'Bill Clinton was governor of his home state of Arkansas .',
            'From humble beginnings Bill Clinton rose to the highest office in the land .',
            'Bill Clinton was involved in a private affair with someone he knew .'
        ]
        s = self.coref.resolve(text)
        self.assertEqual(expected, s)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} port'.format(sys.argv[0]))
        exit()
    port = sys.argv[1]
    del sys.argv[1:]
    unittest.main()
