"""
Skript for training the SpadeClassifier model on the playing_card_dataset.
"""

# IMPORTS
import torch
from dataset import PlayingCardDataset
from torch.utils.data import DataLoader
from src.classifier.model.spadeClassifier import SpadeClassifier
import matplotlib.pyplot as plt
import os


# PARAMS
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 32
DATASET_PATH = "./playing_card_dataset.pt"
PATH_TO_IMAGES = 'data/Images/Images'
PATH_TO_LABELS = 'data/annotation.json'
print(f"MODEL RUNNING ON DEVICE: {device}")


# SAVE GPU FROM SETTING ON FIRE

if device != 'cpu':
    torch.cuda.set_per_process_memory_fraction(0.8, device=0)
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


# DATASET, train/test split, create dataloaders
dataset: PlayingCardDataset = PlayingCardDataset(PATH_TO_IMAGES, PATH_TO_LABELS)
train_set, test_set, _ = torch.utils.data.random_split(dataset, [0.1, 0.1, 0.8])
train_load, test_load = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True), DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True)


# LOAD MODEL
model = SpadeClassifier().to(device)
# model.load_state_dict(torch.load("pretrained_models/model_99.pt", weights_only=True))


# TRAINING PARAMS
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
loss_fn = torch.nn.CrossEntropyLoss()
train_loss = []
test_loss = []
epochs = 200


# TRAINING CODE
def train_one_epoch() -> None:
    torch.cuda.empty_cache()  # TODO save memory
    running_loss = 0.0
    correct = 0.0
    total = 0.0

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
        correct += torch.sum((outputs.argmax(dim=1) == labels.argmax(dim=1))).item()
        total += labels.size(0)

        loss = loss_fn(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        del images, labels, outputs

        running_loss += float(loss)
        if iteration % 15 == 0:
            # Calculate and print accuracy
            accuracy = (correct / total) * 100 if total > 0 else 0
            print(f"Iteration: {iteration}, Loss: {loss.item()}, Accuracy: {accuracy:.2f}%")
    train_loss.append(running_loss / len(train_load))


def test_one_epoch() -> None:
    torch.cuda.empty_cache()  # TODO save memory
    total_correct = 0
    total_samples = 0
    running_loss = 0.0

    model.eval()
    with torch.no_grad():
        for image_batch, label_batch in test_load:
            # Get data and move to the correct device
            images = image_batch.to(device)
            labels = label_batch.to(device)

            # Forward pass
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            running_loss += loss.item()

            # Accuracy calculation
            predicted_classes = outputs.argmax(dim=1)
            true_classes = labels.argmax(dim=1)
            total_correct += (predicted_classes == true_classes).sum().item()
            total_samples += labels.size(0)

    # Calculate average loss and accuracy
    running_loss /= len(test_load)
    accuracy = total_correct / total_samples * 100
    print("--------------------")
    print(f"Test Loss: {running_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")

    test_loss.append(running_loss)


# TRAINING LOOP
for epoch in range(epochs):
    train_one_epoch()
    test_one_epoch()
    torch.cuda.empty_cache()  # Empty memory cache of GPU

    # Save plot and model to file
    os.mkdir(f'pretrained_models/model_{epoch}')
    plt.plot(train_loss, label="Training loss")
    plt.plot(test_loss, label="Test Loss")
    plt.legend()
    plt.savefig(f".pretrained_models/model_{epoch}/plot.png")
    torch.save(model.state_dict(), f"pretrained_models/model_{epoch}/model.pt")

torch.save(model.state_dict(), f"pretrained_models/model_{test_loss[-1]:.4f}_.pt")

