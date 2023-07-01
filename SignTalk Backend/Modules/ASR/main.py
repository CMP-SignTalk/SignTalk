import torch
import torchaudio
from . import feature_extraction


SAMPLE_RATE = 16000

def transcribe(speech_file, model,decoder):
    waveform, sample_rate = torchaudio.load(speech_file)
    if sample_rate != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sample_rate, SAMPLE_RATE)
        waveform = resampler(waveform)
    features = feature_extraction.feature_extraction(waveform)
    model.eval()
    with torch.no_grad():
        output = model(features)
    output = output.transpose(1, 2)
    output = output.contiguous()
    results = decoder(output)
    transcript = " ".join(results[0][0].words).strip()
    return transcript

    