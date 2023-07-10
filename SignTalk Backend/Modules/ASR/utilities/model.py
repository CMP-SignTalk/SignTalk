from torch import nn


class Block(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(Block, self).__init__()
        self.conv = nn.Conv1d(in_channels=in_channels, out_channels=out_channels,
                              kernel_size=kernel_size, stride=stride, padding=padding)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.relu(x)
        return x


class Model(nn.Module):
    def __init__(self, num_classes, num_features=39):
        super(Model, self).__init__()
        self.model = nn.Sequential(
            Block(in_channels=num_features, out_channels=250,
                  kernel_size=48, stride=2, padding=23),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=250,
                  kernel_size=7, stride=1, padding=3),
            Block(in_channels=250, out_channels=2000,
                  kernel_size=32, stride=1, padding=16),
            Block(in_channels=2000, out_channels=2000,
                  kernel_size=1, stride=1, padding=0),
            Block(in_channels=2000, out_channels=num_classes,
                  kernel_size=1, stride=1, padding=0)
        )

    def forward(self, x):
        return nn.functional.log_softmax(self.model(x), dim=1)
