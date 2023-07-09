import torch 
import numpy as np
from scipy.fftpack import dct

class MFCC(torch.nn.Module):
    def __init__(self,sample_rate=16000,window_size_ms = 0.025, hop_length_ms = 0.010, n_mels = 40, n_mfcc = 13, delta= True):
        super(MFCC, self).__init__()
        self.sample_rate = sample_rate
        self.window_size_ms = window_size_ms
        self.hop_length_ms = hop_length_ms
        self.n_mels = n_mels
        self.n_mfcc = n_mfcc
        self.delta = delta
        self.window_size = int(np.floor(self.window_size_ms * self.sample_rate))
        self.hop_length = int(np.floor(self.hop_length_ms * self.sample_rate))
        self.fft_size = 2
        while self.fft_size < self.window_size:
            self.fft_size *= 2


    def preemphasis(self, x):
        # the formula is y[n] = x[n] - 0.97*x[n-1]
        x = torch.cat((x[:,0].unsqueeze(1), x[:,1:] - 0.97*x[:,:-1]), dim=1)
        return x
    
    def windowing(self, x):
        # num_frames = (num_sample - window_size) / hop_length + 1
        num_frames = int((x.shape[1] - self.window_size) / self.hop_length + 1)
        # create hamming window
        window = torch.hamming_window(self.window_size)
        # create frames
        frames = torch.zeros((x.shape[0], num_frames, self.window_size))
        for i in range(num_frames):
            frames[:,i,:] = x[:,i*self.hop_length:i*self.hop_length+self.window_size]
        # apply window
        frames = frames * window
        return frames
    
    def frames_magnitude_spec(self, frames):
        # we first need to compute the fft_size
        # apply fft on each frame
        frames_fft = torch.fft.rfft(frames, n=self.fft_size, dim=2)
        # compute magnitude spectrum
        frames_magnitude_spec = torch.abs(frames_fft)
        return frames_magnitude_spec
    
    def freq_to_mel(self, freq):
        return 2595 * np.log10(1 + freq / 700)

    def mel_to_freq(self, mel):
        return 700 * (10**(mel / 2595) - 1)
    def filterbank(self):
        low_freq_mel = 0
        high_freq_mel = self.freq_to_mel(self.sample_rate / 2)
        mel_points = np.linspace(low_freq_mel, high_freq_mel, self.n_mels + 2)
        hz_points = self.mel_to_freq(mel_points)
        bin = np.floor((self.fft_size + 1) * hz_points / self.sample_rate)
        fbank = np.zeros((self.n_mels, int(np.floor(self.fft_size / 2 + 1))))
        for m in range(1, self.n_mels + 1):
            f_m_minus = int(bin[m - 1])
            f_m = int(bin[m])
            f_m_plus = int(bin[m + 1])
            up = f_m - f_m_minus
            down = f_m_plus - f_m
            for k in range(f_m_minus, f_m):
                fbank[m - 1, k] = (k - bin[m - 1]) / up
            for k in range(f_m, f_m_plus):
                fbank[m - 1, k] = (bin[m + 1] - k) / down
        return fbank

    def frames_mel_spec(self, frames_magnitude_spec):
        fbank = self.filterbank()
        mel_spec = torch.matmul(frames_magnitude_spec, torch.from_numpy(fbank).float().T)
        return mel_spec
    
    def log(self, x):
        return torch.log(x + 1e-20)
    
    def dct(self, x):
        return torch.from_numpy(dct(x.numpy(), axis=2, norm='ortho')).float()
    
    def Delta(self, x):
        # delta = sum over n from n =1 to N (n * (c[n+1] - c[n-1])) / (2 * sum over n from n = 1 to N (n^2))
        # Let's assume N = 1
        delta = torch.zeros(x.shape)
        for i in range(1, x.shape[2] - 1):
            delta[:,:,i] = (x[:,:,i+1] - x[:,:,i-1]) / 2
        return delta
    
    def mfcc(self, x):
        # apply preemphasis
        x = self.preemphasis(x)
        # apply windowing
        frames = self.windowing(x)
        # apply fft -> power spectrum
        frames_magnitude_spec = self.frames_magnitude_spec(frames)
        # apply mel filterbank
        mel_spec = self.frames_mel_spec(frames_magnitude_spec)
        # apply log
        log_mel_spec = self.log(mel_spec)
        # apply dct
        mfcc = self.dct(log_mel_spec)
        # apply delta to get delta mfcc and delta delta mfcc
        if self.delta:
            delta_mfcc = self.Delta(mfcc)
            delta_delta_mfcc = self.Delta(delta_mfcc)
            # select the first n_mfcc coefficients
            return torch.cat((mfcc[:,:,:self.n_mfcc], delta_mfcc[:,:,:self.n_mfcc], delta_delta_mfcc[:,:,:self.n_mfcc]), dim=2)
            
        else:
            return mfcc[:,:,:self.n_mfcc]
    def forward(self, x):
        return self.mfcc(x)




