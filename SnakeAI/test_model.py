import torch
from model import Linear_QNet

model = Linear_QNet(11, 256, 3)

sample_state = torch.rand(11)

prediction = model(sample_state)

print(prediction)