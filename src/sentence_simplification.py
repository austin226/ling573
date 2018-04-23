#!/usr/bin/python3

from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import string

class SentenceSimplifier:
    """Simplifies a single sentence and returns the same text stemmed, and without punctuation or stop words."""

    def process(self, data):

        new_data = ""  # We will build a new text and return it
        stops = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                "now"]

        # Remove all the line feeds from the text
        data = data.replace("\n", " ")

        # Remove punctuation from the text
        data = data.translate(dict.fromkeys(string.punctuation))

        word_list = word_tokenize(data)  # turn sentence into a list of tokens
        new_list = []  # new place to store the words

        for i in range(0, len(word_list)):  # iterate through each token
            word = word_list[i]
            if word not in stops:  # strip out stop words
                new_list.append(word)  # build a new sentence

        stemmer = SnowballStemmer("english")

        new_data = [stemmer.stem(token) for token in new_list]  # stem all the words that we kept

        return " ".join(str(x) for x in new_data)
