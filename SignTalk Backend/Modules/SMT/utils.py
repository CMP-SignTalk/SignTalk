import dill
import os
import gdown

def load_model(filepath):
    with open(filepath, 'rb') as f:
        model = dill.load(f)
    return model

forward_lm_link = "https://drive.google.com/uc?id=1wHuSrrlEDjE9cyMjx4PBlT6pAZkEXdSx"
backward_lm_link = "https://drive.google.com/uc?id=1---4UT0pnASDs1tJjTfTpWjp-IU8r4wd"
forward_ibm1_link = "https://drive.google.com/uc?id=15pfFdUUdekkCVxox5ea85nAZ9xS_1wQa"
backward_ibm1_link = "https://drive.google.com/uc?id=14ojvPyxJnCZjHmHSn5V4HFALaCEF08Tp"
forward_phrase_based_link = "https://drive.google.com/uc?id=1-2CCo2HQDF84sU9eLKel_gCdFt1rBpcD"
backward_phrase_based_link = "https://drive.google.com/uc?id=1-6fRBK_YsA3k1NKyOMtRRUatsQ__jzz1"

models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
forward_lm_path = os.path.join(models_dir, 'forward_lm.pkl')
backward_lm_path = os.path.join(models_dir, 'backward_lm.pkl')
forward_ibm1_path = os.path.join(models_dir, 'forward_ibm1.pkl')
backward_ibm1_path = os.path.join(models_dir, 'backward_ibm1.pkl')
forward_phrase_based_path = os.path.join(models_dir, 'forward_phrase_based.pkl')
backward_phrase_based_path = os.path.join(models_dir, 'backward_phrase_based.pkl')

def download_forward_lm():
    print("Downloading forward_lm.pkl")
    gdown.download(forward_lm_link, forward_lm_path, quiet=False)
    print("forward_lm.pkl downloaded")

def download_backward_lm():
    print("Downloading backward_lm.pkl")
    gdown.download(backward_lm_link, backward_lm_path, quiet=False)
    print("backward_lm.pkl downloaded")

def download_forward_ibm1():
    print("Downloading forward_ibm1.pkl")
    gdown.download(forward_ibm1_link, forward_ibm1_path, quiet=False)
    print("forward_ibm1.pkl downloaded")

def download_backward_ibm1():
    print("Downloading backward_ibm1.pkl")
    gdown.download(backward_ibm1_link, backward_ibm1_path, quiet=False)
    print("backward_ibm1.pkl downloaded")

def download_forward_phrase_based():
    print("Downloading forward_phrase_based.pkl")
    gdown.download(forward_phrase_based_link, forward_phrase_based_path, quiet=False)
    print("forward_phrase_based.pkl downloaded")

def download_backward_phrase_based():
    print("Downloading backward_phrase_based.pkl")
    gdown.download(backward_phrase_based_link, backward_phrase_based_path, quiet=False)
    print("backward_phrase_based.pkl downloaded")

def download_models():
    # Check if the models folder exists and create it if it doesn't exist
    if not os.path.exists(models_dir):
        print("Creating the models folder")
        os.makedirs(models_dir)
        download_forward_lm()
        download_backward_lm()
        download_forward_ibm1()
        download_backward_ibm1()
        download_forward_phrase_based()
        download_backward_phrase_based()
    # Check if all the models are present in the models folder and download the missing ones
    else: 
        if not os.path.exists(forward_lm_path):
            download_forward_lm()
        if not os.path.exists(backward_lm_path):
            download_backward_lm()
        if not os.path.exists(forward_ibm1_path):
            download_forward_ibm1()
        if not os.path.exists(backward_ibm1_path):
            download_backward_ibm1()
        if not os.path.exists(forward_phrase_based_path):
            download_forward_phrase_based()
        if not os.path.exists(backward_phrase_based_path):
            download_backward_phrase_based()

    print("All SMT models downloaded")
