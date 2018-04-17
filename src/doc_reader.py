#!/usr/bin/python3

class DocReader:
    def read_docs(self, input_xml_filename):
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
