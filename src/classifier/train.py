"""
Skript for training the SpadeClassifier model on the playing_card_dataset.
"""

#IMPORTS
import torch
from dataset import PlayingCardDataset
from torch.utils.data import DataLoader
import SpadeClassifier
from mapping import cards
import matplotlib.pyplot as plt

#PARAMS
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 1
DATASET_PATH = "./playing_card_dataset.pt"
print(f"MODEL RUNNING ON DEVICE: {device}")

#DATASET, train/test split, create dataloaders
dataset: PlayingCardDataset = torch.load(DATASET_PATH)
train_set, test_set = torch.utils.data.random_split(dataset, [0.8, 0.2])
train_load, test_load = DataLoader(train_set, batch_size=1, shuffle=True), DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True)

#LOAD MODEL
model = SpadeClassifier.SpadeClassifier(53).to(device)

#TRAINING PARAMS
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
loss_fn = torch.nn.CrossEntropyLoss()
train_loss = []
test_loss = []
epochs = 1

#TRAINING CODE
def train_one_epoch() -> None:
    running_loss = 0.0

    model.train()
    for iteration, data in enumerate(train_load):
        # get data
        images, labels = data
        images.to(device)
        labels.to(device)

        # optimizer and loss function
        optimizer.zero_grad()
        outputs = model(images)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if iteration % 100 == 0:
            print(f"Iteration: {iteration}, Loss: {loss.item()}")

    train_loss.append(running_loss / len(train_load))


def test_one_epoch() -> None:
    running_loss = 0.0

    model.eval()
    for images, labels in test_load:
        images.to(device)
        labels.to(device)

        outputs = model(images)
        loss = loss_fn(outputs, labels)
        running_loss += loss.item()

    running_loss /= len(test_load)
    print("--------------------")
    print(f"Test Loss: {running_loss}\n")

    test_loss.append(running_loss)

#TRAINING LOOP
for epoch in range(epochs):
    train_one_epoch()
    test_one_epoch()