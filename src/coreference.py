#!/usr/bin/python3

import json
from pycorenlp import StanfordCoreNLP

class CoreferenceResolver:
    def __init__(self, port):
        self.port = port

    def resolve(self, sentences):
        #Set up the Stanford Toolkit
        nlp = StanfordCoreNLP('http://localhost:{}'.format(self.port))

        #process all the sentences passed in
        text = ' '.join(sentences)

        output = nlp.annotate(text, properties={
            'annotators': 'coref',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        })

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
                    position = s['position']
                    startIndex = s['startIndex']
                    endIndex = s['endIndex']
                    editedSentence = sentences[position[0] - 1].split()
                    #handle multi-word replacements by removing additional words
                    if startIndex != endIndex-1:
                        editedSentence = editedSentence[0:startIndex] + editedSentence[endIndex-1:]
                    editedSentence[startIndex-1] = replacementText
                    sentences[position[0]-1] = ' '.join(editedSentence)

        return sentences
