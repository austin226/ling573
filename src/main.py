#!/usr/bin/python3

import sys

from content_selection import ContentSelector
from doc_reader import DocReader
from info_ordering import InfoOrder
from sentence_extraction import SentenceExtractor
from sentence_realization import SentenceRealizer
from sentence_simplification import SentenceSimplifier
from sentence_segmentation import SentenceSegmenter
from summarizer import Summarizer

def print_sentences(output_base_dir, topic_id, sentences):
    output_filename = '{}/{}.out'.format(output_base_dir, topic_id)
    with open(output_filename, 'w') as out_f:
        for sentence in sentences:
            out_f.write(sentence + '\n')

def build_content_selector():
    extractor = SentenceExtractor()
    simplifier = SentenceSimplifier()
    segmenter = SentenceSegmenter()

    content_selector = ContentSelector(extractor, simplifier, segmenter)
    return content_selector

def build_summarizer():
    content_selector = build_content_selector()
    info_order = InfoOrder()
    sentence_realizer = SentenceRealizer()
    summarizer = Summarizer(content_selector, info_order, sentence_realizer)
    return summarizer

if __name__ == '__main__':
    # Input to the script is an XML file name
    if len(sys.argv) < 3:
        print('Usage: {} input_xml_filename output_base_dir'.format(sys.argv[0]))
        exit()
    input_xml_filename = sys.argv[1]
    output_base_dir = sys.argv[2]

    # Initialize document reader with AQUAINT and AQUAINT-2 root paths
    doc_reader = DocReader('/dropbox/17-18/573/AQUAINT', '/dropbox/17-18/573/AQUAINT-2')
    summarizer = build_summarizer()

    docsets = doc_reader.read_docs(input_xml_filename)
    for topic_id, sentences in docsets.items():
        summary = summarizer.summarize(sentences)
        print_sentences(output_base_dir, topic_id, summary)

    # TODO evaluation
