import torch


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

##TODO: ct


def feature_extraction(waveform):
    waveform = waveform.unsqueeze(0)
    mean = waveform.mean()
    std = waveform.std()
    waveform = (waveform - mean) / std
    return waveform
