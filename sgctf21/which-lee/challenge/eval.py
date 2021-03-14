#!/usr/bin/env python3

import torch
import torch.nn as nn
from torch.autograd import Function, Variable
from torch.nn.parameter import Parameter
from torchvision import datasets, transforms
import torch.nn.functional as F

import sys

path = sys.argv[1]

NFEATURES=16*16
NHIDDEN=8*8
NCL=5
EPS = 0.00001

# not LeNet
class LeeNet(nn.Module):
    def __init__(self, nFeatures=NFEATURES, nHidden=NHIDDEN, nCl=NCL):
        super().__init__()
        self.fc1 = nn.Linear(nFeatures, nHidden)
        self.fc2 = nn.Linear(nHidden, nCl)
        
    def forward(self, x):
        nBatch = x.size(0)

        # Normal FC network.
        x = x.view(nBatch, -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.layer_norm(x, x.size()[1:], eps=1e-50)
        
        probs = F.softmax(x) 
        
        return probs

# load the model
model = LeeNet()
model.load_state_dict(torch.load("./leenet.ph"))

transform = transforms.Compose([transforms.Resize(16),
                                transforms.CenterCrop(16),
                                transforms.Grayscale(),
                                transforms.ToTensor()])


dataset = datasets.ImageFolder(path, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=True)
images, labels = next(iter(dataloader))
image = images[0].reshape((1, NFEATURES))

y_pred = model(image)
# no flag for you :P
y_pred[:,0] = torch.min(y_pred) - EPS
decision = torch.argmax(y_pred)
print(str(int(decision)))