#!/usr/bin/python3

import sys

from content_selection import ContentSelector
from info_ordering import InfoOrder
from sentence_realization import SentenceRealizer

def parse_docsets(input_xml_filename):
    '''
    Given an XML filename, return a set of docsets,
    each of which is a well-formatted set of sentences
    '''
    # TODO

    # Example
    docsets = [
        ['Docset 1 sentence 1?', 'Docset 1 sentence 2.', 'Docset 1 sentence 3.'],
        ['Docset 2 sentence 1.', 'Docset 2 sentence 2.', 'Docset 2 sentence 3!'],
        ['Docset 3 sentence 1.', 'Docset 3 sentence 2...', 'Docset 3 sentence 3.'],
    ]
    return docsets

if __name__ == '__main__':
    # Input to the script is an XML file name
    if len(sys.argv) < 2:
        print('Usage: {} input_xml_filename'.format(sys.argv[0]))
        exit()
    input_xml_filename = sys.argv[1]

    content_selector = ContentSelector()
    info_order = InfoOrder()
    sentence_realizer = SentenceRealizer()

    docsets = parse_docsets(input_xml_filename)
    for sentences in docsets:
        selected_sentences = content_selector.select(sentences)
        ordered_sentences = info_order.process(selected_sentences)
        realized_sentences = sentence_realizer.process(sentences)
        print(realized_sentences)
