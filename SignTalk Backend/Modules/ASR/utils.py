import os
import torch
from . import model
from torchaudio.models.decoder import ctc_decoder
import gdown

labels = [
    " ",
    *"abcdefghijklmnopqrstuvwxyz",
    "'",
    "*"
]

folder_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

lexicon_file = "lexicon.txt"
lm_file = "lm.bin"
acoustic_file = "states.pth"

lexicon_path = os.path.join(folder_dir, lexicon_file)
lm_path = os.path.join(folder_dir, lm_file)
acoustic_path = os.path.join(folder_dir, acoustic_file)


lexicon_link = "https://drive.google.com/uc?id=1OUbkLInDqboemc9r_MV8Tcbe8rXM-ouz"
lm_link = "https://drive.google.com/uc?id=1-8XsDXaukMtGTpbCWx6GbAaYFwOtx9EB"
acoustic_link = "https://drive.google.com/uc?id=1Jc46RnS9KxffMXDo3Yttw4GV76IiwgL7"


def download_lexicon():
    print("Downloading lexicon")
    gdown.download(lexicon_link, lexicon_path, quiet=False)
    print("Lexicon downloaded")


def download_lm():
    print("Downloading lm")
    gdown.download(lm_link, lm_path, quiet=False)
    print("LM downloaded")


def download_acoustic():
    print("Downloading acoustic")
    gdown.download(acoustic_link, acoustic_path, quiet=False)
    print("Acoustic downloaded")


def download_files():
    if not os.path.exists(folder_dir):
        print("Creating folder")
        os.makedirs(folder_dir)
        download_lexicon()
        download_lm()
        download_acoustic()
    else:
        if not os.path.exists(lexicon_path):
            download_lexicon()
        if not os.path.exists(acoustic_path):
            download_acoustic()
        if not os.path.exists(lm_path):
            download_lm()
    print("All files downloaded")


LM_WEIGHT = 7
WORD_SCORE = -0.26
blank_token = '*'
sil_token = ' '


def load_files():
    download_files()
    acoustic_model = model.Model(num_classes=len(labels))
    acoustic_model.load_state_dict(torch.load(acoustic_path))
    beam_search_decoder = ctc_decoder(
        lexicon=lexicon_path,
        tokens=labels,
        lm=lm_path,
        beam_size_token=len(labels),
        lm_weight=LM_WEIGHT,
        word_score=WORD_SCORE,
        blank_token=blank_token,
        sil_token=sil_token
    )
    return acoustic_model, beam_search_decoder
