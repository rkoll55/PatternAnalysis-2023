import torch.nn as nn
import torch.nn.functional as F
from utils import *

class SuperResolution(nn.Module):
    def __init__(self, upscale_factor=4, channels=1):
        super(SuperResolution, self).__init__()

        self.conv1 = nn.Conv2d(channels, 64, 5, padding=2)
        self.conv2 = nn.Conv2d(64, out_channels, 3, padding=1)
        self.conv3 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.conv4 = nn.Conv2d(out_channels, channels * (upscale_factor ** 2), 3, padding=1)

        #efficient sub-pixel layer
        self.pixel_shuffle = nn.PixelShuffle(upscale_factor)

        # self.pixel_shuffle1 = nn.PixelShuffle(2)
        # self.pixel_shuffle2 = nn.PixelShuffle(2)
        
    def forward(self, x):
        x = F.leaky_relu(self.conv1(x))
        x = F.leaky_relu(self.conv2(x))
        x = F.leaky_relu(self.conv3(x))
        x = F.pixel_shuffle(self.conv4(x), upscale_factor=4)

        # x = self.pixel_shuffle1(self.conv4(x))
        # x = self.pixel_shuffle2(x)
        return x

