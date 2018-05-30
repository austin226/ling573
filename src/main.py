#!/usr/bin/python3

import os
import sys
import traceback

from abbrev_remover import AbbrevRemover
from content_selection import ContentSelector
from coreference import CoreferenceResolver
from doc_reader import DocReader
from info_ordering import InfoOrder
from sentence_extraction import SentenceExtractor
from sentence_realization import SentenceRealizer
from sentence_simplification import SentenceSimplifier
from sentence_segmentation import SentenceSegmenter
from summarizer import Summarizer

def print_sentences(output_base_dir, topic_id, sentences):
    id_part1 = topic_id[:-1]
    id_part2 = topic_id[-1:]
    group_number = 7 # Canvas team number
    output_filename = '{}/{}-A.M.100.{}.{}'.format(output_base_dir, id_part1, id_part2, group_number)

    with open(output_filename, 'w') as out_f:
        for sentence in sentences:
            out_f.write(sentence + '\n')

def build_content_selector():
    extractor = SentenceExtractor(5) # max_sent = 5
    simplifier = SentenceSimplifier()

    content_selector = ContentSelector(extractor, simplifier)
    return content_selector

def build_summarizer(core_nlp_port):
    coreference_resolver = CoreferenceResolver(core_nlp_port)
    segmenter = SentenceSegmenter()
    content_selector = build_content_selector()
    info_order = InfoOrder()
    sentence_realizer = SentenceRealizer()
    summarizer = Summarizer(coreference_resolver, segmenter, content_selector, info_order, sentence_realizer)
    return summarizer

def init_dirs():
    # Create temp directories for intermediate files
    print('Initializing temp dirs...')
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    tmp_dirs = ['docs']
    for d in tmp_dirs:
        os.makedirs('{}/var/{}/'.format(base_dir, d), exist_ok=True)
    print('Initialized.')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: {} input_xml_filename output_base_dir core_nlp_port'.format(sys.argv[0]))
        exit()

    init_dirs()

    input_xml_filename = sys.argv[1]
    output_base_dir = sys.argv[2]
    core_nlp_port = int(sys.argv[3])

    print("Starting summarizer with input_xml_filename='{}', output_base_dir='{}', core_nlp_port='{}'".format(input_xml_filename, output_base_dir, core_nlp_port))

    os.makedirs(output_base_dir, exist_ok=True)

    # Initialize document reader with AQUAINT, AQUAINT-2, and ENG-GW root paths
    doc_reader = DocReader('/dropbox/17-18/573/AQUAINT', '/dropbox/17-18/573/AQUAINT-2', '/dropbox/17-18/573/ENG-GW')
    summarizer = build_summarizer(core_nlp_port)

    print('Reading in documents from "{}"...'.format(input_xml_filename))
    topics_data = doc_reader.read_docs(input_xml_filename)['topics']
    for i, topic in enumerate(topics_data):
        topic_id = topic['id']
        topic_title = topic['title']
        topic_category = topic['category']
        docset = topic['docset']

        print('Summarizing topic "{}" (topic {} of {}, {} documents)...'.format(topic_title, i+1, len(topics_data), len(docset)))

        try:
            summary = summarizer.summarize(topic_id, docset)
        except Exception as e:
            print('Error summarizing docset "{}"'.format(topic_id), file=sys.stderr)
            print(e, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            summary = []
        print_sentences(output_base_dir, topic_id, summary)

    print('Done.')
