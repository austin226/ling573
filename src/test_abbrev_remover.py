#!/usr/bin/python3

import unittest

from abbrev_remover import AbbrevRemover

class AbbrevRemoverTest(unittest.TestCase):
    def setUp(self):
        self.abbrevremover = AbbrevRemover()

    def test_remove(self):
        in_str = 'It is approx. 3 a.m. on Rt. 3 near Mt. Moon.'
        out_str = 'It is approx 3 am on Rt 3 near Mt Moon.'

        self.assertEqual(out_str, self.abbrevremover.remove_abbs(in_str))

if __name__ == '__main__':
    unittest.main()
