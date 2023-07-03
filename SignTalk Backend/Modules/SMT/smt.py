import os  
import sys

# Solve the problem of mandatory put the lm.py, imb1.py, and phrase-based.py in the same directory of server.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import Modules.SMT.utils as utils
import Modules.SMT.ibm1_decoder as ibm1_decoder
import Modules.SMT.phrase_based_decoder as phrase_based_decoder

class SMT:
    def __init__(self):
        # Download the models if they are not present
        utils.download_models()

        # Get the absolute path of the current directory
        folder_dir = os.path.dirname(os.path.abspath(__file__))

        # Load the language models for both ASL Gloss(Forward) and English (Backward)
        self.forward_lm = utils.load_model(os.path.join(folder_dir, 'models', 'forward_lm.pkl'))
        self.backward_lm = utils.load_model(os.path.join(folder_dir, 'models', 'backward_lm.pkl'))

        # Load the translation models for both English to ASL Gloss (Forward) and ASL Gloss to English (Backward)
        self.forward_ibm1 = utils.load_model(os.path.join(folder_dir, 'models', 'forward_ibm1.pkl'))
        self.backward_ibm1 = utils.load_model(os.path.join(folder_dir, 'models', 'backward_ibm1.pkl'))
        self.forward_phrase_based = utils.load_model(os.path.join(folder_dir, 'models', 'forward_phrase_based.pkl'))
        self.backward_phrase_based = utils.load_model(os.path.join(folder_dir, 'models', 'backward_phrase_based.pkl'))

        # Instantiate the decoders
        self.forward_ibm1_translator = ibm1_decoder.Decoder(self.forward_ibm1, self.forward_lm)
        self.backward_ibm1_translator = ibm1_decoder.Decoder(self.backward_ibm1, self.backward_lm)
        self.forward_phrase_based_translator = phrase_based_decoder.Decoder(self.forward_phrase_based, self.forward_lm)
        self.backward_phrase_based_translator = phrase_based_decoder.Decoder(self.backward_phrase_based, self.backward_lm)

    # Translate from English to ASL Gloss
    def forward_translate(self, f):
        e = self.forward_phrase_based_translator.translate(f)
        if  not e : # If the phrase based decoder fails to translate, use the IBM1 decoder
            e = self.forward_ibm1_translator.translate(f)
        return e
    
    # Translate from ASL Gloss to English
    def backward_translate(self, f):
        e = self.backward_phrase_based_translator.translate(f)
        if  not e : # If the phrase based decoder fails to translate, use the IBM1 decoder
            e = self.backward_ibm1_translator.translate(f)
        return e
