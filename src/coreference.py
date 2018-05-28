#!/usr/bin/python3

import json
import sys

from collections import OrderedDict
from pycorenlp import StanfordCoreNLP

class Coreference:
    def __init__(self, data):
        self.replacementText = data['text']
        self.startIndex = data['startIndex']
        self.sentenceIndex = data['sentNum'] - 1
        self.endIndex = data['endIndex']

    def __repr__(self):
        return "{} {} {} {}".format(self.replacementText, self.sentenceIndex, self.startIndex, self.endIndex)

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

        # Limit request length
        output = nlp.annotate(text, properties={
            'annotators': 'coref',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        })

        if not isinstance(output, dict):
            print("Invalid output returned for request length {} ('{}...'): '{}'".format(len(text), text[0:20], output), file=sys.stderr)
            return []

        sentences = []
        for s in output['sentences']:
            sentences.append(OrderedDict([(t['index'], t['originalText']) for t in s['tokens']]))

        coreferences = []
        resolved_sent_indexes_by_replacement_text = {}

        #loop through coreference dictionary
        for r, corefs in output['corefs'].items():
            #find representative mention
            for s in corefs:
                if s['isRepresentativeMention']:
                    replacementText = s['text']
                    representativeSentNum = s['sentNum']
                    break
            if not replacementText:
                continue
            if replacementText not in resolved_sent_indexes_by_replacement_text:
                resolved_sent_indexes_by_replacement_text[replacementText] = set()

            #replace representative mention
            for s in corefs:
                if not s['isRepresentativeMention'] and s['sentNum'] != representativeSentNum:
                    coref = Coreference(s)
                    coref.replacementText = replacementText
                    coreferences.append(coref)

        # Index corefs by sentence
        corefs_by_sentence = {}
        for coref in coreferences:
            if coref.sentenceIndex not in corefs_by_sentence:
                corefs_by_sentence[coref.sentenceIndex] = []
            if coref.sentenceIndex in resolved_sent_indexes_by_replacement_text[coref.replacementText]:
                # Coreference already resolved for this sentence, don't do it more than once
                continue
            resolved_sent_indexes_by_replacement_text[coref.replacementText].add(coref.sentenceIndex)

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
