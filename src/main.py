#!/usr/bin/python3

import sys

from content_selection import ContentSelector
from info_ordering import InfoOrder
from sentence_realization import SentenceRealizer
from summarizer import Summarizer

def parse_docsets(input_xml_filename):
    '''
    Given an XML filename, return a set of docsets,
    each of which is a well-formatted set of sentences
    '''
    # TODO

    # Example
    docsets = {
        # Dict mapping topic ID to sentence list
        'D0901A': ['Docset 1 sentence 1?', 'Docset 1 sentence 2.', 'Docset 1 sentence 3.'],
        'D0912A': ['Docset 2 sentence 1.', 'Docset 2 sentence 2.', 'Docset 2 sentence 3!'],
        'D0934A': ['Docset 3 sentence 1.', 'Docset 3 sentence 2...', 'Docset 3 sentence 3.'],
    }
    return docsets

def print_sentences(output_base_dir, topic_id, sentences):
    output_filename = '{}/{}.out'.format(output_base_dir, topic_id)
    with open(output_filename, 'w') as out_f:
        for sentence in sentences:
            out_f.write(sentence + '\n')

if __name__ == '__main__':
    # Input to the script is an XML file name
    if len(sys.argv) < 3:
        print('Usage: {} input_xml_filename output_base_dir'.format(sys.argv[0]))
        exit()
    input_xml_filename = sys.argv[1]
    output_base_dir = sys.argv[2]

    content_selector = ContentSelector()
    info_order = InfoOrder()
    sentence_realizer = SentenceRealizer()
    summarizer = Summarizer(content_selector, info_order, sentence_realizer)

    docsets = parse_docsets(input_xml_filename)
    for topic_id, sentences in docsets.items():
        summary = summarizer.summarize(sentences)
        print_sentences(output_base_dir, topic_id, summary)

    # TODO evaluation
