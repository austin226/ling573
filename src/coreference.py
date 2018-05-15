#!/usr/bin/python3

import json
from collections import OrderedDict
from pycorenlp import StanfordCoreNLP

class Coreference:
    def __init__(self, data):
        self.replacementText = data['text']
        self.startIndex = data['startIndex']
        self.sentenceIndex = data['sentNum'] - 1
        self.endIndex = data['endIndex']

    def __repr__(self):
        return "{} {} {} {} {}".format(self.text, self.replacementText, self.startIndex, self.sentenceIndex, self.endIndex)

class CoreferenceResolver:
    def __init__(self, port):
        self.port = port

    def replace_tokens(self, tokens, replacementText, startIndex, endIndex):
        for i in range(startIndex, endIndex):
            if i not in tokens:
                # Don't do a replacement if the range does not exist
                return tokens

        output = OrderedDict()
        for k, v in tokens.items():
            if k < startIndex or k >= endIndex:
                output[k] = v
            elif k == startIndex:
                output[k] = replacementText
        return output

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
        for s in output['sentences']:
            sentences.append(OrderedDict([(t['index'], t['originalText']) for t in s['tokens']]))

        coreferences = []

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
                    coref = Coreference(s)
                    coref.replacementText = replacementText
                    coreferences.append(coref)

        # Index corefs by sentence
        corefs_by_sentence = {}
        for coref in coreferences:
            if coref.sentenceIndex not in corefs_by_sentence:
                corefs_by_sentence[coref.sentenceIndex] = []
            corefs_by_sentence[coref.sentenceIndex].append(coref)

        # Replace tokens in each sentence
        for sentenceIndex, corefs in corefs_by_sentence.items():
            for coref in corefs:
                tokens = sentences[sentenceIndex]
                sentences[sentenceIndex] = self.replace_tokens(tokens, coref.replacementText, coref.startIndex, coref.endIndex)

        # Turn sentences back into strings
        text_sentences = []
        for s in sentences:
            tokens = list(s.values())
            text_sentences.append(' '.join(tokens))
        return text_sentences
