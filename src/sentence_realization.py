#!/usr/bin/python3

class SentenceRealizer:
    '''
    The goal of this class is to "create a fluent, readable, compact output",
    converting a set of sentences into a coherent narrative.
    '''

    def process(self, sentences, simplified):
        '''
        Use both full and simplified format for each sentence to form a coherent list of sentences
        '''

        # Remove spaces before any non-word
        sentences = [self.remove_extra_spaces(s) for s in sentences]
        return sentences

    def remove_extra_spaces(self, sentence):
        tokens = sentence.split(' ')
        output = []
        for t in tokens:
            if t[0].isalnum() or t == '--' or t == '_':
                output.append(t)
            elif not output:
                # No tokens in output yet
                output.append(t)
            else:
                # Token is not a word, append to last token in output
                output[-1] += t
        return ' '.join(output)
