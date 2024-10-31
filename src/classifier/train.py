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
        # Get data and move to the correct device
        images, labels = data
        images = images.to(device)
        labels = labels.to(device)

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if iteration % 500 == 0:
            print(f"Iteration: {iteration}, Loss: {loss.item()}")


def test_one_epoch() -> None:
    labeled_correctly = 0
    running_loss = 0.0

    model.eval()
    with torch.no_grad():
        for images, labels in test_load:
            # Get data and move to the correct device
            images = images.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            running_loss += loss.item()
            if outputs.argmax() == labels.argmax():
                labeled_correctly += 1

    running_loss /= len(test_load)
    print("--------------------")
    print(f"Test Loss: {running_loss}\n")
    print(f"Accuracy: {labeled_correctly / len(test_load) * 100:.2f}%")

    test_loss.append(running_loss)

#TRAINING LOOP
for epoch in range(epochs):
    train_one_epoch()
    test_one_epoch()

plt.plot(train_loss, label="Training loss")
plt.plot(test_loss, label="Test Loss")
plt.legend()
plt.show()

torch.save(model, f"./models/model_{next(reversed(test_loss))}")