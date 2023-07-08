# Path: Integration\Decoder\phrase_based.py
import re
import warnings
from nltk.translate.stack_decoder import StackDecoder

class Decoder:
    def __init__(self, translation_model, e_language_model = None):
        self.stack_decoder = StackDecoder(translation_model.f_e_phrase_table, e_language_model)

    def translate(self, f):
        # Remove special characters with regex, convert to lowercase, and split into tokens
        f = re.sub(r'[^a-zA-Z0-9\s]', '', f)
        f_tokens = f.lower().split()
        # stack_decoder.translate raise a warning if the source sentence contains words not in the phrase table'
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=Warning)
                e_tokens = self.stack_decoder.translate(f_tokens)
        except Warning:
            e_tokens = []
        e = ' '.join(e_tokens)
        return e