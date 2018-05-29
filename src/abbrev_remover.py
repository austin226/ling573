#!/usr/bin/python3

import re

class AbbrevRemover:
    def __init__(self):
        self.abbrevs = ["a.m.", "acct.", "A.D.", "approx.", "Ave.", "B.A.", "B.C.", "Blvd.", "Bros.", "B.S.", "C.E.", "cf.",
                   "cm.", "Dr.", "e.g.", "et al.", "etc.", "fig.", "ft.", "gal.", "I.D.", "i.e.", "in.", "km.", "L.A.",
                   "M.A.", "M.B.A.", "mi.", "m.p.h.", "Mr.", "Mrs.", "M.S.", "Ms.", "Mt.", "N.Y.", "no.", "nos.",
                   "p.", "Ph.D", "p.m.", "pp.", "qv.", "Rd.", "Rt.", "R.S.V.P.", "sq.", "St.", "U.S.", "U.S.A.",
                   "V.I.P.", "vol."] 
    
    def remove_abbs(text: str):
        if "." not in text or text == "":  # Do not traverse text if it contains no full stops
            return text
        else:
            for abb in self.abbrevs:
                if abb not in text:  # Disregard abbreviations not present in text
                    continue
                else:
                    abb_stripped = abb.replace('.', '')  # default is the abbreviation with capitals intact
                    text = text.replace(abb, abb_stripped)  # assume abbrevs do not end sentences
            match = re.search("([A-Z].)[ ]*([A-Z].) [A-Z]", text)
            if match:
                text = text.replace(match.group(1), match.group(1).replace('.', ''))
                text = text.replace(match.group(2), match.group(2).replace('.', ''))
            return text
