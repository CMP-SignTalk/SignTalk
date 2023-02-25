from language_model import language_model
from translation_model import translation_model
from decoder import decoder
from utils import load_corpus

def smt_translation(source_sentence):
    """
    A function that uses SMT to translate a source sentence to a target sentence.

    Args:
    - source_sentence (str): The source sentence to be translated.

    Returns:
    - target_sentence (str): The translated sentence.
    """
    # load the source and target corpus
    source_corpus = load_corpus("path to source corpus")
    target_corpus = load_corpus("path to target corpus")

    # calculate the models probabilities
    language_model_probabilities = language_model(target_corpus)
    translation_model_probabilities = translation_model(source_corpus, target_corpus)

    # find the most likely translation of the source sentence
    target_sentence = decoder(source_sentence, translation_model_probabilities, language_model_probabilities)

    return target_sentence

print(smt_translation('I play piano.'))