import json
from pycorenlp import StanfordCoreNLP


#Testing only, to be removed once news sentences are passed in
sentences = ['Bill Clinton was governor of Arkansas.', 'From humble beginnings he rose to the highest office in the land.',
             'Clinton was involved in a private affair.']
#Set up the Stanford Toolkit
nlp = StanfordCoreNLP('http://localhost:9000')

#process all the sentences passed in
text = ' '.join(sentences)

output = nlp.annotate(text, properties={'annotators': 'coref','pipelineLanguage': 'en','outputFormat': 'json'})

#print(output['corefs'])

#testing before
print(sentences)

#loop through coreference dictionary
for r in output['corefs']:
    #find representative mention
    for s in output['corefs'][r]:
        if s['isRepresentativeMention']:
            replacementText = s['text']
            break
    #replace representative mention
    for s in output['corefs'][r]:
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
#testing after
print(sentences)