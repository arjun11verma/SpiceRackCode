import torch
import torch.nn as nn
import random

spice_dict = {
    "Basil" : 0,
    "Cumin": 1
}

reverse_spice_dict = {
    0 : "Basil",
    1 : "Cumin"
}

class SpeechNet(nn.Module):
    def __init__(self, BUFFER_SIZE, NUM_CLASSES=8):
        super(SpeechNet, self).__init__()

        self.conv1d = nn.Conv1d(1, 10, 8, 1)
        self.nonlinear = nn.ReLU()
        self.maxpool_one = nn.MaxPool1d(8, 2)
        self.conv1d_two = nn.Conv1d(10, 15, 6, 1)
        self.maxpool_two = nn.MaxPool1d(6, 4)
        self.flatten = nn.Flatten()
        self.linear_one = nn.Linear(180, 24)
        self.linear_two = nn.Linear(24, NUM_CLASSES)
        self.logSoftmax = nn.LogSoftmax(dim=1)
    
    def forward(self, X):
        ret_val = self.conv1d(X)
        ret_val = self.nonlinear(ret_val)
        ret_val = self.maxpool_one(ret_val)
        ret_val = self.conv1d_two(ret_val)
        ret_val = self.nonlinear(ret_val)
        ret_val = self.maxpool_two(ret_val)
        ret_val = self.flatten(ret_val)

        ret_val = self.linear_one(ret_val)
        ret_val = self.nonlinear(ret_val)
        ret_val = self.linear_two(ret_val)

        ret_val = self.logSoftmax(ret_val)

        return ret_val

def train_model(model, optimizer, spice_data, num_epochs = 20, NUM_CLASSES = 2):
    model.train()

    for i in range(num_epochs):
        random.shuffle(spice_data)
        total_loss = 0

        for label_data in spice_data:
            data, label = label_data
            label = int(spice_dict[label])
            model.zero_grad()

            y_onehot = torch.zeros(NUM_CLASSES)
            y_onehot[label] = 1
            y_onehot = torch.unsqueeze(y_onehot, 1)

            output = model.forward(data)

            loss = torch.neg(output).matmul(y_onehot)

            total_loss += loss

            loss.backward()
            optimizer.step()
        print(f'Loss at epoch {i}: {total_loss}')

    print("Done training!")

    return model

def predict_spice(model, data):
    with torch.no_grad():
        output = model.forward(data)

    output = torch.squeeze(output)
    prediction = torch.argmax(output)
    
    return prediction.item()

def save_trained_model(model):
    torch.save(model.state_dict(), "./spice_model.pt")

def load_model(BUFFER_SIZE, NUM_CLASSES = 8):
    model = SpeechNet(BUFFER_SIZE, NUM_CLASSES=NUM_CLASSES)
    model.load_state_dict(torch.load("./spice_model.pt"))
    model.eval()
    return model




