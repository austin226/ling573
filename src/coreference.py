#!/usr/bin/python3

import json
from pycorenlp import StanfordCoreNLP

class CoreferenceResolver:
    def __init__(self, port):
        self.port = port

    def resolve(self, sentences):
        #Set up the Stanford Toolkit
        nlp = StanfordCoreNLP('http://localhost:{}'.format(self.port))

        resolved = []

        for sentence in sentences:
            resolved_sentence = sentence
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
                        startIndex = s['startIndex']
                        endIndex = s['endIndex']

                        tokens = output['sentences'][0]['tokens']
                        editedSentence = [t['originalText'] for t in tokens]
                        #handle multi-word replacements by removing additional words
                        if startIndex != endIndex-1:
                            editedSentence = editedSentence[0:startIndex] + editedSentence[endIndex-1:]
                        resolved_sentence = ' '.join(editedSentence)
            resolved.append(resolved_sentence)

        return resolved
