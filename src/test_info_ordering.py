#!/usr/bin/python3

import unittest
from info_ordering import InfoOrder

class InfoOrderTest(unittest.TestCase):
    def setUp(self):
        self.info_ord = InfoOrder()

    def testSentenceSimilarity(self):
        sentences = [
            "The pumped line can't fear the push.",
            "The green sheep coughed hourly.",
            "The small letter whispered quirkily.",
            "The yellow book talked gracefully.",
        ]
        expected_similarity = [
            1.0,
            0.11435786435786437,
            0.1414141414141414,
            0.12638888888888888,
            0.12380952380952381,
            1.0,
            0.12777777777777777,
            0.12631578947368421,
            0.11688311688311688,
            0.0992063492063492,
            1.0,
            0.1875,
            0.11666666666666667,
            0.10964912280701754,
            0.1875,
            1.0,
        ]
        sim_idx = 0

        for s1 in sentences:
            for s2 in sentences:
                sim = self.info_ord.sentence_similarity(s1, s2)
                self.assertEqual(expected_similarity[sim_idx], sim)
                sim_idx += 1

if __name__ == '__main__':
    unittest.main()
