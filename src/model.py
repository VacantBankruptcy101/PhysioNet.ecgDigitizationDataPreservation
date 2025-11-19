import torch
import torch.nn as nn

class ECGResNet(nn.Module):
    def __init__(self, out_dim=1000):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 32, 7, 2, 3), nn.ReLU(), nn.BatchNorm2d(32),
            nn.Conv2d(32, 64, 3, 2, 1), nn.ReLU(), nn.BatchNorm2d(64),
            nn.Conv2d(64, 128, 3, 2, 1), nn.ReLU(), nn.BatchNorm2d(128),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, out_dim)
        )
    def forward(self, x):
        x = self.encoder(x)
        x = self.head(x)
        return x
