from deepmultilingualpunctuation import PunctuationModel

class TextProcessing():

    def restore_punctuation(text):
        model = PunctuationModel(model = "kredor/punctuate-all")
        result = model.restore_punctuation(text)
        return result

if __name__ == "__main__":
    pass