"""Sign & Speak Training Script

This script uses transfer learning on a ResNet18 model from the PyTorch model zoo
to train an image classification model for a limited set of sign language words
and phrases. It is compatible with Amazon SageMaker, which can be used to run
training and hyperparameter tuning jobs from this script.

The input consists of 3x3 grid images of video frames, organized into folders
for each label (e.g., a folder named 'cat' contains all training images for
the sign for cat). 

The code is based on this tutorial:
https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
"""

import time
import copy
import logging
import sys
import argparse
import json
import os

import numpy as np
import torch
from torch.utils.data.sampler import SubsetRandomSampler
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision import models


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def save_model(model, model_dir):
    """
    Saves the entire PyTorch model in the model
    artifact directory.
    """
    logger.info("Saving the model.")
    path = os.path.join(model_dir, 'model.pth')
    torch.save(model, path)


def save_classes(class_to_idx, output_dir):
    """
    Saves the dictionary of indices assigned to
    labels in the output directory as a JSON file.
    """
    logger.info("Saving classes.")
    with open(os.path.join(output_dir, "class_indices.json"), "w") as file_handle:
        json.dump(class_to_idx, file_handle)


def train(args):
    """
    Splits the data set into training and validation sets, transforms the data,
    and runs the training epochs.
    """

    # Define a data transformation similar to the one used to train the original ResNet model
    data_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load data from an image folder structure (one folder per label)
    dataset = ImageFolder(args.data_dir, transform=data_transform)
    class_names = dataset.classes

    # Shuffle and define split of data into training and validation sets
    validation_split = .1
    shuffle_dataset = True
    dataset_size = len(dataset)
    indices = list(range(dataset_size))
    split = int(np.floor(validation_split * dataset_size))
    if shuffle_dataset :
        np.random.seed(args.seed)
        np.random.shuffle(indices)
    train_indices, val_indices = indices[split:], indices[:split]
    dataset_sizes = {'train': len(train_indices),
                    'val': len(val_indices)}
    samplers = {'train': SubsetRandomSampler(train_indices),
            'val': SubsetRandomSampler(val_indices)}
    
    dataloaders = {x: DataLoader(dataset, batch_size=args.batch_size, 
                                            sampler=samplers[x])
                for x in ['train', 'val']}


    # Load and set up pretrained ResNet model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_ft = models.resnet18(pretrained=True)
    num_ftrs = model_ft.fc.in_features
    logger.info("Number of classes is {}".format(len(class_names)))
    model_ft.fc = nn.Linear(num_ftrs, len(class_names))
    model_ft = model_ft.to(device)
    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=args.lr, momentum=args.momentum)

    # Decay learning rate
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=args.step_size, gamma=args.gamma)

    since = time.time()
    best_model_wts = copy.deepcopy(model_ft.state_dict())
    best_acc = 0.0
    num_epochs = args.epochs

    for epoch in range(num_epochs):
        logger.info('Epoch {}/{}'.format(epoch, num_epochs - 1))
        logger.info('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model_ft.train()  # Set model to training mode
            else:
                model_ft.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer_ft.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model_ft(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer_ft.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                exp_lr_scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            logger.info('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # Track the best validation accuracy
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model_ft.state_dict())

    time_elapsed = time.time() - since
    logger.info('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    logger.info('Best val Acc: {:4f}'.format(best_acc))

    # Load best model weights and save this model
    model_ft.load_state_dict(best_model_wts)
    save_model(model_ft, args.model_dir)
    save_classes(dataset.class_to_idx, args.model_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Parameters specific to the deep learning model
    parser.add_argument('--batch-size', type=int, default=4, help='input batch size for training (default: 4)')
    parser.add_argument('--epochs', type=int, default=25, help='number of epochs to train (default: 25)')
    parser.add_argument('--lr', type=float, default=0.001, help='learning rate (default: 0.001)')
    parser.add_argument('--momentum', type=float, default=0.9, help='SGD momentum (default: 0.9)')
    parser.add_argument('--seed', type=int, default=42, help='random seed (default: 42)')
    parser.add_argument('--step-size', type=int, default=7, help='step size (default: 7)')
    parser.add_argument('--gamma', type=float, default=0.1, help='gamma (default: 0.1)')

    # Amazon SageMaker container environment variables
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'], help='path to the directory to write model artifacts to')
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAINING'], help='path to the directory containing the training data')

    train(parser.parse_args())
    