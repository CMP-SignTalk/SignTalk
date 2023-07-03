# Path: Integration\TM\phrase_based.py
from math import log
from nltk.translate import PhraseTable
from nltk.translate.phrase_based import phrase_extraction

class PhraseBasedModel:
    def __init__(self, f_corpus, e_corpus, f_e_alignment):
        self.f_corpus = f_corpus
        self.e_corpus = e_corpus
        self.f_e_alignment = f_e_alignment
        # Phrase Pairs Extraction
        self.phrase_table = None
        # Phrase Pairs Scoring
        self.e_phrase_count = None 
        self.f_e_phrase_count = None 
        self.score_to_f_e_phrase = None 
        self.phrase_translation_score = None 
        self.f_e_phrase_table = None

    # Extract all the possible phrase pairs from the given sentence pairs using the IBM1 model and store them to the phrase_table
    def extrat_phrase_pairs(self):
        self.phrase_table = [] # Contains tuples of the form (f_start, f_end, f_phrase, e_phrase)
        for i in range(len(self.f_corpus)):
            srctext = self.f_corpus[i]
            trgtext = self.e_corpus[i]          
            alignment = self.f_e_alignment[i]
            phrases = phrase_extraction(srctext, trgtext, alignment)
            self.phrase_table.extend(phrases)
    
    # Score the phrase pairs using the relative frequency
    def score_phrase_pairs(self):
        """
        Calculate the relative frequency by calculating the count of each e_phrase and the count of 
        each pair of f_phrase and e_phrase. Then, dividing the count of each pair by the count of its 
        corresponding e_phrase to get the relative frequency.
        """
        self.e_phrase_count = {} # Contains the count of each e_phrase
        self.f_e_phrase_count = {} # Contains the count of each pair of f_phrase, e_phrase
        self.score_to_f_e_phrase = [] # Contains tuples of the form (phrase_translation_score, (f_phrase, e_phrase))
        self.phrase_translation_score = {} 
        self.f_e_phrase_table = PhraseTable()

        for phrase in sorted(self.phrase_table):
            f_phrase = phrase[2]
            e_phrase = phrase[3]

            # Increment the count of the e_phrase 
            if(e_phrase not in self.e_phrase_count):
                self.e_phrase_count[e_phrase] = 1
            else:
                self.e_phrase_count[e_phrase] += 1
            
            # Increment the count of the pair of f_phrase, e_phrase
            if((f_phrase, e_phrase) not in self.f_e_phrase_count):            
                self.f_e_phrase_count[(f_phrase, e_phrase)] = 1
            else:            
                self.f_e_phrase_count[(f_phrase, e_phrase)] += 1    

        # Calculate the phrase translation score for each pair of f_phrase, e_phrase
        for f_e_phrase, count in sorted(self.f_e_phrase_count.items()):
            self.phrase_translation_score[f_e_phrase] = ( 1.0 * count ) / self.e_phrase_count[f_e_phrase[1]]
            self.score_to_f_e_phrase.append((self.phrase_translation_score[f_e_phrase], f_e_phrase))    

        # Store the phrases with their scores in the phrase table
        for (score, (f_phrase, e_phrase)) in sorted(self.score_to_f_e_phrase)[::-1]: 
            f_phrase = tuple(f_phrase.split())
            e_phrase = tuple(e_phrase.split())
            self.f_e_phrase_table.add(f_phrase, e_phrase, log(score))   
   