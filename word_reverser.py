def reverse_words(text):
    words = text.split()
    reversed_words = [word[::-1] for word in words]
    return ' '.join(reversed_words)

class WordReverser:
    @staticmethod
    def process(text):
        return reverse_words(text)

    @staticmethod
    def get_name():
        return "Word Reverser"

    @staticmethod
    def get_description():
        return "Reverses each word in the text while maintaining word order."