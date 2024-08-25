import re

def reverse_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    reversed_sentences = sentences[::-1]
    return ' '.join(reversed_sentences)

class SentenceReverser:
    @staticmethod
    def process(text):
        return reverse_sentences(text)

    @staticmethod
    def get_name():
        return "Sentence Reverser"

    @staticmethod
    def get_description():
        return "Reverses the order of sentences in the text."