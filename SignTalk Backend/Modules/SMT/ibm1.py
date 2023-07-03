# Path: Integration\TM\ibm1.py
from collections import defaultdict

class IBMModel1:
    def __init__(self, f_corpus, e_corpus):
        self.f_corpus = f_corpus
        self.e_corpus = e_corpus
        self.f_vocab = set()
        self.e_vocab = set()
        self.translation_table = None
        self.translation_tuple = None
        self.e_f_alignment = None
        self.f_e_alignment = None

    # Preprocess the corpus and collect the vocabulary
    def _preprocess(self, sentences):
        vocabs = set()
        tokenized_sentences = []
        for sentence in sentences:
            sentence =  sentence.lower()
            tokenized_senetence = sentence.split()
            for token in tokenized_senetence:
                vocabs.add(token)
            tokenized_sentences.append(tokenized_senetence) 
        return vocabs, tokenized_sentences

    def preprocess(self):
        self.f_vocab, self.f_corpus = self._preprocess(self.f_corpus)
        self.e_vocab, self.e_corpus = self._preprocess(self.e_corpus)

    # Fill the tranlsation table with the translation probabilities.
    def train(self, num_iters=10000, total_displacement = 0.00000001):
        # Initialize the translation table with uniform probabilities - It will be used in the IBM1 decoders
        self.translation_table = defaultdict(lambda: defaultdict(lambda: 1 / len(self.e_vocab)))
        self.translation_tuple = {} # This is a 1-d dictionary of tuples to be used for extracting alignment
        for f_i in self.f_vocab:
            for e_j in self.e_vocab:
                    self.translation_tuple[(f_i, e_j)] = 1.0 / len(self.e_vocab)

        # Run EM algorithm for num_iters iterations or until the total displacement is less than total_displacement
        while(num_iters != 0):
            total_difference = 0.0
            count = defaultdict(lambda: defaultdict(float))
            total = defaultdict(float)
            s_total = defaultdict(float)
            # Expectation Step
            for (_ , (f, e)) in enumerate(zip(self.f_corpus, self.e_corpus)):
                for e_j in e:
                    for f_i in f:
                        s_total[e_j] += self.translation_table[f_i][e_j]
                        
                for e_j in e:
                    for f_i in f:
                        c = self.translation_table[f_i][e_j] / s_total[e_j]
                        count[f_i][e_j] += c
                        total[f_i] += c
            
            # Maximization Step
            for f_i in self.f_vocab:
                for e_j in self.e_vocab:
                    total_difference += abs(self.translation_table[f_i][e_j] - count[f_i][e_j] / total[f_i])
                    # Update the translation table
                    self.translation_table[f_i][e_j] = count[f_i][e_j] / total[f_i]
                    # Update the 1-d dictionary of tuples with the same values as the translation table
                    self.translation_tuple[(f_i, e_j)] = count[f_i][e_j] / total[f_i]

            if(total_difference < total_displacement):
                break
            num_iters-=1
    
    # Get the alignment for a given sentence pair
    def _get_alignment(self, f, e):
        """
        f: a list of soucre sentence tokens
        e: a list of target sentence tokens
        return: e_f_alignment, f_e_alignment
        """
        e_f_alignment = []
        f_e_alignment = []
        # For each word in the target sentence, find the word in the source sentence that has the maximum probability.
        for e_i in range(len(e)):
            max_prob = -1
            max_f = -1
            for f_i in range(len(f)):
                if(self.translation_tuple[(f[f_i], e[e_i])] > max_prob):
                    max_f = f_i
                    max_prob = self.translation_tuple[(f[f_i], e[e_i])]
            e_f_alignment.append((e_i, max_f))
            f_e_alignment.append((max_f, e_i))
        return e_f_alignment, f_e_alignment
    
    # Get the alignment for each sentence pair in the corpus
    def align(self):
        self.e_f_alignment = []
        self.f_e_alignment = []
        for (_ , (f, e)) in enumerate(zip(self.f_corpus, self.e_corpus)):
            e_f_alignment, f_e_alignment = self._get_alignment(f, e)
            self.e_f_alignment.append(e_f_alignment)
            self.f_e_alignment.append(f_e_alignment)
