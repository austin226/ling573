#!/usr/bin/python3

import unittest
from sentence_realization import SentenceRealizer

class SentenceRealizerTest(unittest.TestCase):
    def setUp(self):
        self.sr = SentenceRealizer()

    def test_basic_order(self):
        sentences = [
            "These four defendants fell in behind the couple Wednesday as These four defendants marched two blocks to a courthouse where four white police officers pleaded innocent to murder charges in the shooting death of the Diallos ' son , a 22-year-old street vendor from Guinea with no criminal record . four white police officers heard cheers , too -- from scores of four white police officers off-duty colleagues , most of four white police officers white .",
            "NEW YORK _ the people knowledgeable about the case have told associates that the people knowledgeable about the case attention was initially drawn to Diallo when the people knowledgeable about the case saw Amadou Diallo standing on the stoop of a the Bronx apartment building and thought the people knowledgeable about the case saw Amadou Diallo peering into the window of a first-floor apartment , according to people with knowledge of the case . the people knowledgeable about the case told associates that the people knowledgeable about the case grew more suspicious when two of the people knowledgeable about the case got out of the people knowledgeable about the case car to question Amadou Diallo and Amadou Diallo retreated into the building 's vestibule , the people knowledgeable about the case said on Tuesday 's .",
            "NEW YORK _ Diallo 's parents to meet with the Bronx district attorney on Wednesday to receive a preview of the criminal charges that the grand jury voted to bring against the four New York City police officers who killed their son 's seven weeks ago .",
            "Stephen Brounstein , the lawyer for Boss , and James Culleton , the lawyer for Murphy , Stephen Brounstein , the lawyer for Boss , and James Culleton , the lawyer for Murphy said that Stephen Brounstein , the lawyer for Boss , and James Culleton , the lawyer for Murphy clients heard gunfire and saw McMellon on the ground , leading Stephen Brounstein , the lawyer for Boss , and James Culleton , the lawyer for Murphy to assume that McMellon had been shot .",
            "NEW YORK _ Now that the four police officers charged with killing Amadou Diallo have been arraigned , the next step in the legal process will come at the end of the month , when the four police officers charged with killing Amadou Diallo lawyers and the Bronx prosecutors are to appear before a judge to set a schedule for the pretrial proceedings .",
            "KUWAIT CITY, November 2 Xinhua -- More than 40 percent of Kuwaiti women are obese and suffer from other chronic ailments such as vein-hardening, diabetes and hypertension, local press reported today, citing a Kuwaiti psychologist.",
        ]
        expected_output = [
            "These four defendants fell in behind the couple Wednesday as These four defendants marched two blocks to a courthouse where four white police officers pleaded innocent to murder charges in the shooting death of the Diallos' son, a 22-year-old street vendor from Guinea with no criminal record. four white police officers heard cheers, too -- from scores of four white police officers off-duty colleagues, most of four white police officers white.",
            "The people knowledgeable about the case have told associates that the people knowledgeable about the case attention was initially drawn to Diallo when the people knowledgeable about the case saw Amadou Diallo standing on the stoop of a the Bronx apartment building and thought the people knowledgeable about the case saw Amadou Diallo peering into the window of a first-floor apartment, according to people with knowledge of the case. the people knowledgeable about the case told associates that the people knowledgeable about the case grew more suspicious when two of the people knowledgeable about the case got out of the people knowledgeable about the case car to question Amadou Diallo and Amadou Diallo retreated into the building's vestibule, the people knowledgeable about the case said on Tuesday's.",
            "Diallo's parents to meet with the Bronx district attorney on Wednesday to receive a preview of the criminal charges that the grand jury voted to bring against the four New York City police officers who killed their son's seven weeks ago.",
            "Stephen Brounstein, the lawyer for Boss, and James Culleton, the lawyer for Murphy, Stephen Brounstein, the lawyer for Boss, and James Culleton, the lawyer for Murphy said that Stephen Brounstein, the lawyer for Boss, and James Culleton, the lawyer for Murphy clients heard gunfire and saw McMellon on the ground, leading Stephen Brounstein, the lawyer for Boss, and James Culleton, the lawyer for Murphy to assume that McMellon had been shot.",
            "Now that the four police officers charged with killing Amadou Diallo have been arraigned, the next step in the legal process will come at the end of the month, when the four police officers charged with killing Amadou Diallo lawyers and the Bronx prosecutors are to appear before a judge to set a schedule for the pretrial proceedings.",
            "More than 40 percent of Kuwaiti women are obese and suffer from other chronic ailments such as vein-hardening, diabetes and hypertension, local press reported today, citing a Kuwaiti psychologist.",
        ]
        simplified = [] # TODO
        processed = self.sr.process(sentences, simplified)

        self.assertEqual(expected_output, processed)

if __name__ == '__main__':
    unittest.main()
