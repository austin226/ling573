#!/usr/bin/python3

import re
import sys

from lxml import etree as ET
from html.parser import HTMLParser, HTMLParseError

class Aquaint1Parser(HTMLParser):
    # See document type definition at https://catalog.ldc.upenn.edu/docs/LDC2002T31/
    output = {
        'type': 'news story',   # Default to 'news story'; otherwise will be 'miscellaneous text'
        'keywords': [],
        'headlines': [],
        'datelines': [],
        'paragraphs': [],
    }
    on_correct_document = False
    reading_docno = False
    reading_doctype = False
    reading_body = False
    reading_slug = False
    reading_headline = False
    reading_text = False

    def get_output(self):
        return self.output

    def set_doc_id(self, doc_id):
        self.doc_id = doc_id

    # Override HTMLParser methods

    def handle_starttag(self, tag, attrs):
        if tag == 'doc':
            for name, value in attrs:
                if name == 'id' and value == 'doc_id':
                    self.on_correct_document = True
        elif tag == 'docno':
            self.reading_docno = True
        elif self.on_correct_document:
            if tag == 'doctype':
                self.reading_doctype = True
            elif tag == 'body':
                self.reading_body = True
            elif tag == 'slug':
                self.reading_slug = True
            elif tag == 'headline':
                self.reading_headline = True
            elif tag == 'text':
                self.reading_text = True

    def handle_data(self, data):
        if self.reading_docno:
            if data.strip() == self.doc_id:
                self.on_correct_document = True
        elif self.on_correct_document:
            if self.reading_doctype:
                self.output['type'] = data.strip().lower()
            elif self.reading_body:
                if self.reading_slug:
                    # TODO parse slugs into multiple keywords, not just 1
                    self.output['keywords'].append(data.strip())
                elif self.reading_headline:
                    self.output['headlines'].append(data.strip())
                elif self.reading_text:
                    # TODO parse text into multiple paragraphs, not just 1
                    self.output['paragraphs'].append(data.strip())

    def handle_endtag(self, tag):
        if tag == 'docno':
            self.reading_docno = False
        elif tag == 'doc':
            self.on_correct_document = False
        elif self.on_correct_document:
            if tag == 'doctype':
                self.reading_doctype = False
            elif tag == 'body':
                self.reading_body = False
            elif tag == 'slug':
                self.reading_slug = False
            elif tag == 'headline':
                self.reading_headline = False
            elif tag == 'text':
                self.reading_text = False

class DocReader:
    xml_cache = {}

    def __init__(self, aq_root, aq2_root, eng_gw_root):
        '''
        aq_root: AQUAINT root path
        aq2_root: AQUAINT-2 root path
        eng_gw_root: ENG-GW root path
        '''

        self.aq_root = aq_root
        self.aq2_root = aq2_root
        self.eng_gw_root = eng_gw_root

        aq_regex = '([A-Z]+)(\d{4})(\d{4})\.(\d{4})'
        self.aq_pattern = re.compile(aq_regex, re.IGNORECASE)

        aq2_regex = '([^_]+)_([^_]+)_(\d{4})(\d{4})\.(\d{4})'
        self.aq2_pattern = re.compile(aq2_regex, re.IGNORECASE)

    def resolve_path(self, doc_id):
        '''
        Converts a document ID into an absolute path
        Returns: (path, format_name)
        '''
        match = self.aq_pattern.match(doc_id)
        if match:
            # doc_id matches AQUAINT
            # Example: APW19990421.0284 is located at
            # {aq_root}/apw/1999/19990421_APW_ENG

            # ('APW', '1999', '0421', '0284')
            publisher, year, volume, doc_num = match.groups()
            if publisher == 'NYT':
                suffix = publisher
            elif publisher == 'XIE':
                suffix = 'XIN_ENG'
            else:
                suffix = '{}_ENG'.format(publisher)

            path = '{}/{}/{}/{}{}_{}'.format(self.aq_root, publisher.lower(), year, year, volume, suffix)
            return (path, 'AQUAINT')

        match = self.aq2_pattern.match(doc_id)
        if match:
            # doc_id matches AQUAINT-2
            # Example: XIN_ENG_20050415.0040 is located at
            # {aq2_root}/data/xin_eng/xin_eng_200504.xml
            # ('XIN', 'ENG', '2005', '0415', '0040')

            publisher, lang, year, volume, doc_num = match.groups()

            if int(year) > 2005:
                # ENG-GW, not AQUAINT-2
                # Example: APW_ENG_20061002.1245 is located at
                # {eng_gw_root}/data/apw_eng/apw_eng_200610.gz
                path = '{}/data/{}_{}/{}_{}_{}{}.gz'.format(self.eng_gw_root, publisher.lower(), lang.lower(), publisher.lower(), lang.lower(), year, volume[:2])
                return (path, 'ENG-GW')

            path = '{}/data/{}_{}/{}_{}_{}{}.xml'.format(self.aq2_root, publisher.lower(), lang.lower(), publisher.lower(), lang.lower(), year, volume[:2])
            return (path, 'AQUAINT-2')

        raise ValueError('doc_id "{}" is invalid'.format(doc_id))

    def parse_doc(self, path, format_name, doc_id):
        if format_name == 'AQUAINT' or format_name == 'ENG-GW':
            # SGML format
            sgml = self.clip_sgml(path, doc_id, format_name)
            parser = Aquaint1Parser(convert_charrefs=True)
            parser.set_doc_id(doc_id)

            try:
                parser.feed(sgml)
            except HTMLParseError as e:
                print('Error parsing document "{}" from file "{}" (format: {})'.format(doc_id, path, format_name), file=sys.stderr)
                print(e, file=sys.stderr)
                # Skip this file
                return None
            return parser.get_output()

        elif format_name == 'AQUAINT-2':
            # XML format
            if path in self.xml_cache:
                tree = self.xml_cache[path]
            else:
                try:
                    tree = ET.parse(path)
                except ET.XMLSyntaxError:
                    print('Error parsing XML from file {}, skipping'.format(path), file=sys.stderr)
                    return None
                self.xml_cache[path] = tree
            docstream = tree.getroot()

            # Get doc element by ID
            doc = docstream.findall(".//*[@id='{}']".format(doc_id))[0]

            # DTD reference: /corpora/LDC/LDC08T25/data/apw_eng/a2_newswire_xml.dtd
            doc_type = doc.get('type')
            keywords = [k.text.strip() for k in doc.findall('KEYWORD')]
            # DATE_TIME is never actually declared, so skip it
            headlines = [h.text.strip() for h in doc.findall('HEADLINE')]
            datelines = [d.text.strip() for d in doc.findall('DATELINE')]

            text = doc.find('TEXT')
            if text is not None:
                paras = text.findall('P')
                if len(paras):
                    paragraphs = [p.text.strip() for p in paras]
                else:
                    paragraphs = [text.text]

            doc_out = {
                'type': doc_type,
                'keywords': keywords,
                'headlines': headlines,
                'datelines': datelines,
                'paragraphs': paragraphs
            }
            return doc_out

        else:
            raise ValueError('Unknown format: "{}"'.format(format_name))

    def clip_sgml(self, path, doc_id, format_name):
        output_lines = []
        with open(path, 'r') as f:
            reading_doc = False
            lines = f.readlines()
            if format_name == 'AQUAINT':
                for i, line in enumerate(lines):
                    if line.startswith('<DOCNO>') and doc_id in line:
                        reading_doc = True
                        output_lines.append(lines[i-1])
                    elif line.startswith('</DOCNO>'):
                        output_lines.extend(lines[i:i+1])
                        break
                    if reading_doc:
                        output_lines.append(line)
            elif format_name == 'ENG-GW':
                for i, line in enumerate(lines):
                    if line.startswith('<DOC') and doc_id in line:
                        reading_doc = True
                    elif line.startswith('</DOC>'):
                        output_lines.append(line)
                        break
                    if reading_doc:
                        output_lines.append(line)
            else:
                raise ValueError('Unknown format: "{}"'.format(format_name))
            return ("\n").join(output_lines)

    def read_docs(self, input_xml_filename, max_docs = None):
        '''
        Given an XML filename, return a set of docsets,
        each of which is a well-formatted set of sentences
        '''

        parsed_doc_count = 0

        tree = ET.parse(input_xml_filename)
        tac_task_data = tree.getroot()
        num_topics = len(tac_task_data)

        topics_out = []
        i = 0
        for topic in tac_task_data:
            i += 1
            print('Parsing docset {} of {}...'.format(i, num_topics))
            topic_id = topic.get('id')
            topic_category = topic.get('category')
            topic_title = topic.find('title').text.strip()
            topic_docset = topic.find('docsetA')

            docs_out = {}
            for doc in topic_docset:
                if max_docs is not None and parsed_doc_count >= max_docs:
                    continue
                doc_id = doc.get('id')
                doc_path, doc_format = self.resolve_path(doc_id)
                try:
                    if doc_format == 'AQUAINT':
                        continue
                    doc_contents = self.parse_doc(doc_path, doc_format, doc_id)
                    parsed_doc_count += 1
                except FileNotFoundError:
                    print('Error loading file "{}"'.format(doc_path), file=sys.stderr)
                    # Skip this file
                    continue
                docs_out[doc_id] = doc_contents
            topics_out.append({
                'id': topic_id,
                'title': topic_title,
                'category': topic_category,
                'docset': docs_out
            })
        return {'topics': topics_out}
