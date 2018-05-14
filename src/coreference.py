#!/usr/bin/python3

import json
from pycorenlp import StanfordCoreNLP

class CoreferenceResolver:
    def __init__(self, port):
        self.port = port

    def resolve(self, text):
        '''
        This will accept a block of text, and return
        a list of sentences with coreferences resolved.
        '''

        #Set up the Stanford Toolkit
        nlp = StanfordCoreNLP('http://localhost:{}'.format(self.port))

        output = nlp.annotate(text, properties={
            'annotators': 'coref',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        })

        sentences = []

        #loop through coreference dictionary
        for r, corefs in output['corefs'].items():
            #find representative mention
            for s in corefs:
                if s['isRepresentativeMention']:
                    replacementText = s['text']
                    break
            #replace representative mention
            for s in corefs:
                if not s['isRepresentativeMention']:
                    sentIdx = s['sentNum'] - 1
                    startIndex = s['startIndex']
                    endIndex = s['endIndex']

                    tokens = output['sentences'][sentIdx]['tokens']
                    editedSentence = [t['originalText'] for t in tokens]
                    #handle multi-word replacements by removing additional words
                    if startIndex != endIndex-1:
                        editedSentence = editedSentence[0:startIndex] + editedSentence[endIndex-1:]
                    sentences.append(' '.join(editedSentence))

        return sentences
