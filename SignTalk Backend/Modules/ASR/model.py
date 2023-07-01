from torch import nn


class Model(nn.Module):
    def __init__(self, num_classes, num_features=1, type=0):
        features = 250 if type == 0 else num_features
        super(Model, self).__init__()
        self.acoustic_model = nn.Sequential(
            nn.Conv1d(in_channels=features,
                      out_channels=250, kernel_size=48, stride=2, padding=23),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=250,
                      kernel_size=7, stride=1, padding=3),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=250, out_channels=2000,
                      kernel_size=32, stride=1, padding=16),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=2000, out_channels=2000,
                      kernel_size=1, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv1d(in_channels=2000, out_channels=num_classes,
                      kernel_size=1, stride=1, padding=0),
            nn.ReLU(inplace=True),
        )
        if type == 0:
            extra_layer = nn.Sequential(
                nn.Conv1d(in_channels=num_features, out_channels=250,
                          kernel_size=250, stride=160, padding=45),
                nn.ReLU(inplace=True),
            )
            self.acoustic_model = nn.Sequential(
                extra_layer, self.acoustic_model)

    def forward(self, x):
        return nn.functional.log_softmax(self.acoustic_model(x), dim=1)
