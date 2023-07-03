import math
import numpy as np
from nltk import bigrams, trigrams, FreqDist
from collections import Counter

class Unigram:
    def __init__(self, corpus):
        self.corpus = corpus

    def preprocess(self, min_freq=1):
        self.vocabs = set()
        self.sentences = []
        for sentence in self.corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            # Collect the vocabs
            for token in sentence:
                self.vocabs.add(token)
            self.sentences.append(sentence)
        # Filter out low-frequency tokens from the vocabulary
        counter = Counter(token for sentence in self.sentences for token in sentence)
        for token, freq in counter.items():
            if freq < min_freq:
                self.vocabs.remove(token)
        self.vocabs = list(self.vocabs)

        # Add the <unk> token to handle unknown words -> words that are out of the vocabulary of the language model.
        self.vocabs.append("<unk>")
        self.vocabs_length = len(self.vocabs)
        self.index_to_word = {i: word for i, word in enumerate(list(self.vocabs))}
        self.word_to_index = {word: i for i, word in self.index_to_word.items()}
        self.counts = np.zeros(self.vocabs_length, dtype=int)

    # Fill the 1D array with the appropriate counts.
    def train(self):
        for sentence in self.sentences:
            for word in sentence:
                if word in self.vocabs:
                    self.counts[self.word_to_index[word]] += 1
                else: # unknown word
                    self.counts[self.word_to_index["<unk>"]] += 1
    
    # Calculates the add-k smoothed probabilities - To handle the unseen words.
    # P(word) = (Count(word) + k) / (N + kV)
    def calc_probability(self, word, k=1):
        if word in self.vocabs: # The word is in the vocabulary of the language model. 
            return (self.counts[self.word_to_index[word]] + k) / (np.sum(self.counts) + k*self.vocabs_length)
        else:
            return (self.counts[self.word_to_index["<unk>"]] + k) / (np.sum(self.counts) + k*self.vocabs_length)
    
    def calc_log_probability(self, word):
        return np.log(self.calc_probability(word))

    def calc_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 1
        for i in range(0, len(sentence)):
            probability *= self.calc_probability(sentence[i])            
        return probability

    def calc_log_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 0
        for i in range(0, len(sentence)):
            probability += self.calc_log_probability(sentence[i])       
        return probability
    
    # Required for the Phrase-Based Decoder.
    def probability(self, sentence):
        sentence = ' '.join(sentence)
        return self.calc_log_sentence_probability(sentence)

    # Calculates the change in log probability of a sentence if a given string is appended to it.
    def probability_change(self, sentence, phrase):
        sentence = ' '.join(sentence.trg_phrase)
        phrase = ' '.join(phrase)
        previous_probability = self.calc_log_sentence_probability(sentence)
        current_probability = self.calc_log_sentence_probability(sentence + " " + phrase)
        return current_probability - previous_probability

    def perplexity(self, test_corpus):
        test_sentences = []
        for sentence in test_corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            test_sentences.append(sentence)
        N = 0 # total number of tokens
        log_likelihood = 0
        for sentence in test_sentences:
            for word in sentence:
                N += 1
                log_likelihood += self.calc_log_probability(word)
        perplexity = math.exp(-log_likelihood / N)
        return perplexity
    
###########################################################################################################
class Bigram:
    def __init__(self, corpus):
        self.corpus = corpus

    def preprocess(self, min_freq=1):
        self.vocabs = set()
        self.sentences = []
        for sentence in self.corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            # Collect the vocabs
            for token in sentence:
                self.vocabs.add(token)
            self.sentences.append(sentence)
        # Filter out low-frequency tokens from the vocabulary
        counter = Counter(token for sentence in self.sentences for token in sentence)
        for token, freq in counter.items():
            if freq < min_freq:
                self.vocabs.remove(token)
        self.vocabs = list(self.vocabs)

        # Add the <unk> token to handle unknown words -> words that are out of the vocabulary of the language model.
        self.vocabs.append("<unk>")
        self.vocabs_length = len(self.vocabs)
        self.index_to_word = {i: word for i, word in enumerate(list(self.vocabs))}
        self.word_to_index = {word: i for i, word in self.index_to_word.items()}
        self.counts = np.zeros((self.vocabs_length, self.vocabs_length), dtype=int)

    # Fill the 2D array with the appropriate counts
    def train(self):
        for sentence in self.sentences:
            sentence_bigrams = bigrams(sentence)
            sentence_bigrams_fd = FreqDist(sentence_bigrams)
            for bigram , frequency in sentence_bigrams_fd.items():
                if bigram[0] in self.vocabs and bigram[1] in self.vocabs:
                    self.counts[self.word_to_index[bigram[0]], self.word_to_index[bigram[1]]] += frequency
                elif bigram[0] in self.vocabs and bigram[1] not in self.vocabs:
                    self.counts[self.word_to_index[bigram[0]], self.word_to_index["<unk>"]] += frequency
                elif bigram[0] not in self.vocabs and bigram[1] in self.vocabs:
                    self.counts[self.word_to_index["<unk>"], self.word_to_index[bigram[1]]] += frequency                
                else:
                    self.counts[self.word_to_index["<unk>"], self.word_to_index["<unk>"]] += frequency
    
    # Calculates the add-k smoothed probabilities - To handle the unseen words.
    # P(word1, word2) = (Count(word1, word2) + k) / (Count(word1) + kV)
    def calc_probability(self, word1, word2, k=1):
        if (word1 in self.vocabs) and (word2 in self.vocabs):
            return (self.counts[self.word_to_index[word1], self.word_to_index[word2]] + k)/(np.sum(self.counts[self.word_to_index[word1], :]) + k*self.vocabs_length)
        elif (word1 in self.vocabs) and (word2 not in self.vocabs):
            return (self.counts[self.word_to_index[word1], self.word_to_index["<unk>"]] + k) / (np.sum(self.counts[self.word_to_index[word1], :]) + k*self.vocabs_length)
        elif (word1 not in self.vocabs) and (word2 in self.vocabs):
            return (self.counts[self.word_to_index["<unk>"], self.word_to_index[word2]] + k) / (np.sum(self.counts[self.word_to_index["<unk>"], :]) + k*self.vocabs_length)
        else:
            return (self.counts[self.word_to_index["<unk>"], self.word_to_index["<unk>"]] + k) / (np.sum(self.counts[self.word_to_index["<unk>"], :]) + k*self.vocabs_length)

    def calc_log_probability(self, word1, word2):
        return np.log(self.calc_probability(word1, word2))
    
    def calc_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 1
        for i in range(1, len(sentence)):
            probability *= self.calc_probability(sentence[i-1], sentence[i])           
        return probability
    
    def calc_log_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 0
        for i in range(1, len(sentence)):
            probability += self.calc_log_probability(sentence[i-1], sentence[i])       
        return probability

    # Required for the Phrase-Based Decoder.
    def probability(self, sentence):
        sentence = ' '.join(sentence)
        return self.calc_log_sentence_probability(sentence)
    
    # Calculates the change in log probability of a sentence if a given string is appended to it.
    def probability_change(self, sentence, phrase):
        sentence = ' '.join(sentence.trg_phrase)
        phrase = ' '.join(phrase)
        previous_probability = self.calc_log_sentence_probability(sentence)
        current_probability = self.calc_log_sentence_probability(sentence + " " + phrase)
        return current_probability - previous_probability

    def perplexity(self, test_corpus):
        test_sentences = []
        for sentence in test_corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            test_sentences.append(sentence)
        N = 0 # total number of bigrams
        log_likelihood = 0
        for sentence in test_sentences:
            for i in range(1, len(sentence)):
                N += 1
                log_likelihood += self.calc_log_probability(sentence[i-1], sentence[i])
        perplexity = math.exp(-log_likelihood / N)
        return perplexity
    
###########################################################################################################
class Trigram:
    def __init__(self, corpus):
        self.corpus = corpus

    def preprocess(self, min_freq=1):
        self.vocabs = set()
        self.sentences = []
        for sentence in self.corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            # Collect the vocabs
            for token in sentence:
                self.vocabs.add(token)
            self.sentences.append(sentence)
        # Filter out low-frequency tokens from the vocabulary
        counter = Counter(token for sentence in self.sentences for token in sentence)
        for token, freq in counter.items():
            if freq < min_freq:
                self.vocabs.remove(token)
        self.vocabs = list(self.vocabs)

        # Add the <unk> token to handle unknown words -> words that are out of the vocabulary of the language model.
        self.vocabs.append("<unk>")
        self.vocabs_length = len(self.vocabs)
        self.index_to_word = {i: word for i, word in enumerate(list(self.vocabs))}
        self.word_to_index = {word: i for i, word in self.index_to_word.items()}
        vocab_pairs = [(v1, v2) for v1 in list(self.vocabs) for v2 in list(self.vocabs)]
        self.index_to_pair = {i: pair for i, pair in enumerate(vocab_pairs)}
        self.pair_to_index = {pair: i for i, pair in self.index_to_pair.items()}
        self.counts = np.zeros((self.vocabs_length * self.vocabs_length, self.vocabs_length), dtype=int)

    # Fill the 2D matrix with the appropriate counts.
    def train(self):
        for sentence in self.sentences:
            sentence_trigrams = trigrams(sentence)
            sentence_trigrams_fd = FreqDist(sentence_trigrams)
            for trigram, frequency in sentence_trigrams_fd.items():
                # 111 110 101 100 011 010 001 000
                if trigram[0] in self.vocabs and trigram[1] in self.vocabs and trigram[2] in self.vocabs:
                    self.counts[self.pair_to_index[(trigram[0], trigram[1])], self.word_to_index[trigram[2]]] += frequency 
                elif trigram[0] in self.vocabs and trigram[1] in self.vocabs and trigram[2] not in self.vocabs:
                    self.counts[self.pair_to_index[(trigram[0], trigram[1])], self.word_to_index["<unk>"]] += frequency
                elif trigram[0] in self.vocabs and trigram[1] not in self.vocabs and trigram[2] in self.vocabs:
                    self.counts[self.pair_to_index[(trigram[0], "<unk>")], self.word_to_index[trigram[2]]] += frequency
                elif trigram[0] in self.vocabs and trigram[1] not in self.vocabs and trigram[2] not in self.vocabs:
                    self.counts[self.pair_to_index[(trigram[0], "<unk>")], self.word_to_index["<unk>"]] += frequency
                elif trigram[0] not in self.vocabs and trigram[1] in self.vocabs and trigram[2] in self.vocabs:
                    self.counts[self.pair_to_index[("<unk>", trigram[1])], self.word_to_index[trigram[2]]] += frequency
                elif trigram[0] not in self.vocabs and trigram[1] in self.vocabs and trigram[2] not in self.vocabs:
                    self.counts[self.pair_to_index[("<unk>", trigram[1])], self.word_to_index["<unk>"]] += frequency
                elif trigram[0] not in self.vocabs and trigram[1] not in self.vocabs and trigram[2] in self.vocabs:
                    self.counts[self.pair_to_index[("<unk>", "<unk>")], self.word_to_index[trigram[2]]] += frequency
                else:
                    self.counts[self.pair_to_index[("<unk>", "<unk>")], self.word_to_index["<unk>"]] += frequency

    # Calculates the add-k smoothed probabilities - To handle the unseen words.
    # P(word1, word2, word3) = (Count(word1, word2, word3) + k) / (Count(word1, word2) + kV)
    def calc_probability(self, word1, word2, word3, k=1):
        if (word1, word2) in self.pair_to_index and word3 in self.vocabs:
            return (self.counts[self.pair_to_index[(word1, word2)], self.word_to_index[word3]] + k) / (np.sum(self.counts[self.pair_to_index[(word1, word2)], :]) + k*self.vocabs_length)
        elif (word1, word2) in self.pair_to_index and word3 not in self.vocabs:
            return (self.counts[self.pair_to_index[(word1, word2)], self.word_to_index["<unk>"]] + k) / (np.sum(self.counts[self.pair_to_index[(word1, word2)], :]) + k*self.vocabs_length)
        elif (word1, word2) not in self.pair_to_index and word3 in self.vocabs:
            return (self.counts[self.pair_to_index[("<unk>", "<unk>")], self.word_to_index[word3]] + k) / (np.sum(self.counts[self.pair_to_index[("<unk>", "<unk>")], :]) + k*self.vocabs_length)
        else:
            return (self.counts[self.pair_to_index[("<unk>", "<unk>")], self.word_to_index["<unk>"]] + k) / (np.sum(self.counts[self.pair_to_index[("<unk>", "<unk>")], :]) + k*self.vocabs_length)

    def calc_log_probability(self, word1, word2, word3):
        return np.log(self.calc_probability(word1, word2, word3))    

    def calc_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 1
        for i in range(2, len(sentence)):
            probability *= self.calc_probability(sentence[i-2], sentence[i-1], sentence[i])       
        return probability
    
    def calc_log_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 0
        for i in range(2, len(sentence)):
            probability += self.calc_log_probability(sentence[i-2], sentence[i-1], sentence[i])       
        return probability
    
    # Required for the Phrase-Based Decoder.
    def probability(self, sentence):
        sentence = ' '.join(sentence)
        return self.calc_log_sentence_probability(sentence)
    
    # Calculates the change in log probability of a sentence if a given string is appended to it.
    def probability_change(self, sentence, phrase):
        sentence = ' '.join(sentence.trg_phrase)
        phrase = ' '.join(phrase)
        previous_probability = self.calc_log_sentence_probability(sentence)
        current_probability = self.calc_log_sentence_probability(sentence + " " + phrase)
        return current_probability - previous_probability

    def perplexity(self, test_corpus):
        test_sentences = []
        for sentence in test_corpus:
            sentence = sentence.lower()
            sentence = sentence.split()
            sentence.insert(0, "<s>")
            sentence.append("</s>")
            test_sentences.append(sentence)
        N = 0
        log_likelihood = 0
        for sentence in test_sentences:
            for i in range(2, len(sentence)):
                N += 1
                log_likelihood += self.calc_log_probability(sentence[i-2], sentence[i-1], sentence[i])
        perplexity = math.exp(-log_likelihood / N)
        return perplexity
        
###########################################################################################################
class LM:
    def __init__(self, corpus):
        self.unigram_lm = Unigram(corpus)
        self.bigram_lm = Bigram(corpus)
        self.trigram_lm = Trigram(corpus)
        
    def preprocess(self, min_freq=1):
        self.unigram_lm.preprocess(min_freq)
        self.bigram_lm.preprocess(min_freq)
        self.trigram_lm.preprocess(min_freq)

    def train(self):
        self.unigram_lm.train()
        self.bigram_lm.train()
        self.trigram_lm.train()

    def calc_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 1
        lambda1 = 0.2
        lambda2 = 0.3
        lambda3 = 0.5
        for i in range(2, len(sentence)):
            trigram_probability = self.trigram_lm.calc_probability(sentence[i-2], sentence[i-1], sentence[i])
            bigram_probability = self.bigram_lm.calc_probability(sentence[i-1], sentence[i])
            unigram_probability = self.unigram_lm.calc_probability(sentence[i])
            probability *= (lambda1 * trigram_probability + lambda2 * bigram_probability + lambda3 * unigram_probability)
        return probability        

    def calc_log_sentence_probability(self, sentence):
        sentence =  sentence.lower()
        sentence = sentence.split()
        sentence.insert(0, "<s>")
        sentence.insert(len(sentence), "</s>")
        probability = 0
        lambda1 = 0.2
        lambda2 = 0.3
        lambda3 = 0.5
        for i in range(2, len(sentence)):
            trigram_probability = self.trigram_lm.calc_probability(sentence[i-2], sentence[i-1], sentence[i])
            bigram_probability = self.bigram_lm.calc_probability(sentence[i-1], sentence[i])
            unigram_probability = self.unigram_lm.calc_probability(sentence[i])
            probability += np.log(lambda1 * trigram_probability + lambda2 * bigram_probability + lambda3 * unigram_probability)
        return probability
    
    # Required for the Phrase-Based Decoder.
    def probability(self, sentence):
        sentence = ' '.join(sentence)
        return self.calc_log_sentence_probability(sentence)

    # Calculates the change in log probability of a sentence if a given string is appended to it.
    def probability_change(self, sentence, phrase):
        sentence = ' '.join(sentence.trg_phrase)
        phrase = ' '.join(phrase)
        previous_probability = self.calc_log_sentence_probability(sentence)
        current_probability = self.calc_log_sentence_probability(sentence + " " + phrase)
        return current_probability - previous_probability
