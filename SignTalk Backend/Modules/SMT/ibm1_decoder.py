# Path: Integration\Decoder\ibm1.py
class Decoder:
    def __init__(self, translation_model, language_model = None):
        self.translation_model = translation_model
        self.language_model = language_model

    def translate(self, f):
        f_tokens = f.lower().split()
        e_tokens = []
        for token in f_tokens:
            translation_probs = self.translation_model.translation_table[token]
            # print('token: ', token)
            # print('sorted_translation_probs: ', dict(sorted(translation_probs.items(), key=lambda kv: kv[1], reverse=True)))
            # print(' ')
            if translation_probs:
                if self.language_model:
                    # Choose best translation token (not just the most probable)
                    best_e_token = max(translation_probs, key=lambda e_token: translation_probs[e_token] * self.language_model.calc_sentence_probability(' '.join(e_tokens + [e_token])))
                else:
                    # Choose most probable translation token
                    best_e_token = max(translation_probs, key = lambda e_token: translation_probs[e_token]) 
                e_tokens.append(best_e_token)
            else:
                e_tokens.append(token)

        e_tokens = [token for token in e_tokens if token is not None]
        e = ' '.join(e_tokens)
        return e
    