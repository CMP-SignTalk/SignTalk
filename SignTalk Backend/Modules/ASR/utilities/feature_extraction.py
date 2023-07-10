import torch
from .mfcc.mfcc import MFCC

class Norm(torch.nn.Module):
    '''
    Normalizes a tensor along its last dimension

    Args:
        tensor (torch.Tensor): tensor to normalize
    Returns:
        normalized tensor
    '''

    def forward(self, tensor):
        mean = tensor.mean(-1, keepdim=True)
        std = tensor.std(-1, keepdim=True)
        return (tensor - mean) / std

def feature_extraction(waveform):
    transform = torch.nn.Sequential(
        MFCC(),
        Norm()
    )
    return transform(waveform).unsqueeze(0)








