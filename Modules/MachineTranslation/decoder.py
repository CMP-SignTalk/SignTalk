def decoder(source_sentence, translation_model_probabilities, language_model_probabilities):
    """
    A function that finds the argmax of P(f,a|e)P(e) over all possible target sentences.

    Args:
    - source_sentence (str): The source sentence to be translated.
    - translation_model_probabilities (dict): A dictionary mapping each source sentence to a dictionary of translation probabilities for each possible target sentence.
    - language_model_probabilities (dict): A dictionary mapping each target sentence to its probability.

    Returns:
    - target_sentence (str): The target sentence with the highest probability.
    """
    # TODO: implement a decoder for finding the argmax of P(f,a|e)P(e) over all possible target sentences
    target_sentence = "I PLAY PIANO"
    return target_sentence
