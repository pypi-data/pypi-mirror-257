import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from decent_dp.utils import setupenv
rank, world_size = setupenv()

from tqdm import tqdm
from loguru import logger
import torch
import torchvision
from torch.utils.data import DistributedSampler, DataLoader
import torch.distributed as dist
from decent_dp.ddp import DecentralizedDataParallel as ddp

dist.init_process_group()

model = torch.nn.Sequential(
    torch.nn.Flatten(),
    torch.nn.Linear(784, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100, 10),
)
model = ddp(model, topology='ring')

train_dataset = torchvision.datasets.MNIST(
    train=True,
    download=True,
    root='.',
    transform=torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
)
valid_dataset = torchvision.datasets.MNIST(
    train=False,
    download=True,
    root='.',
    transform=torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
)
train_sampler = DistributedSampler(train_dataset)
valid_sampler = DistributedSampler(valid_dataset, shuffle=False)

train_ds = DataLoader(train_dataset,
                      batch_size=256 // world_size, sampler=train_sampler)
valid_ds = DataLoader(valid_dataset, batch_size=256 // world_size, sampler=valid_sampler)

optim = torch.optim.Adam(model.parameters(), lr=0.003)
loss_fn = torch.nn.CrossEntropyLoss()

for epoch in range(10):
    model.train()
    avg_loss = 0.0
    avg_acc = 0.0
    with tqdm(train_ds, desc=f'Epoch {epoch}', disable=rank!=0) as t:
        for step, (data, target) in enumerate(t):
            optim.zero_grad()
            output = model(data)
            loss = loss_fn(output, target)
            loss.backward()
            optim.step()
            model.sync()
            
            avg_loss += loss.item()
            avg_acc += (output.argmax(1) == target).float().mean().item()
            t.set_postfix({'loss': f'{avg_loss / (step + 1):.5f}', 'acc': f'{avg_acc / (step + 1):.5f}'})
    if rank == 0:
        logger.info(f'Training loss: {avg_loss / (step + 1):.5f}, accuracy: {avg_acc / (step + 1):.5f}')
    
    model.global_avg()

    with torch.no_grad():
        model.eval()
        avg_loss = 0.0
        avg_acc = 0.0
        for step, (data, target) in enumerate(valid_ds):
            output = model(data)
            loss = loss_fn(output, target)
            avg_loss += loss.item()
            avg_acc += (output.argmax(1) == target).float().mean().item()
        if rank == 0:
            logger.info(f'Validation loss: {avg_loss / (step + 1):.5f}, accuracy: {avg_acc / (step + 1):.5f}')
