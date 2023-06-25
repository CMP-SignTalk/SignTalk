# from Modules.SMT.utils import *
# import Modules.SMT.ibm1 as ibm1
# import Modules.SMT.phrase_based as phrase_based

from utils import *
import ibm1 as ibm1
import phrase_based as phrase_based

class SMT:
    def __init__(self):
        # Load the language models 
        self.bigram_lm_forward = load_model('models/lm/bigram_lm_forward.pkl')
        self.bigram_lm_backward = load_model('models/lm/bigram_lm_backward.pkl')

        # Load the translation models
        self.ibm1_forward = load_model('models/tm/ibm1_forward.pkl')
        self.ibm1_backward = load_model('models/tm/ibm1_backward.pkl')
        self.phrase_based_forward = load_model('models/tm/phrase_based_forward.pkl')
        self.phrase_based_backward = load_model('models/tm/phrase_based_backward.pkl')

        # Instantiate the decoders
        self.ibm1_forward_translator = ibm1.Decoder(self.ibm1_forward, self.bigram_lm_forward)
        self.ibm1_backward_translator = ibm1.Decoder(self.ibm1_backward, self.bigram_lm_backward)
        self.phrase_based_forward_translator = phrase_based.Decoder(self.phrase_based_forward, self.bigram_lm_forward)
        self.phrase_based_backward_translator = phrase_based.Decoder(self.phrase_based_backward, self.bigram_lm_backward)

    # Translate from English to ASL Gloss
    def forward_translate(self, f):
        e = self.phrase_based_forward_translator.translate(f)
        if  not e : # If the phrase based decoder fails to translate, use the IBM1 decoder
            e = self.ibm1_forward_translator.translate(f)
        return e
    
    # Translate from ASL Gloss to English
    def backward_translate(self, f):
        e = self.phrase_based_backward_translator.translate(f)
        if  not e : # If the phrase based decoder fails to translate, use the IBM1 decoder
            e = self.ibm1_backward_translator.translate(f)
        return e
