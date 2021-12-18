from numpy.core.defchararray import mod
import speech_buffering
import random
import speech_to_text
import torch
from torch import optim
import torch.nn as nn

import speech_to_text

def main():
    pass

if __name__ == "__main__":
    spice_data = speech_buffering.load_buffer("Basil") + speech_buffering.load_buffer("Cumin")

    NUM_CLASSES = 2

    model = speech_to_text.SpeechNet(128, NUM_CLASSES=NUM_CLASSES)
    optimizer = optim.SGD(model.parameters(), lr = 0.0001)

    model = speech_to_text.train_model(model, optimizer, spice_data, num_epochs=50)

    model.eval()

    num_correct = 0
    num_avail = len(spice_data)
    for data_line in spice_data:
        data, label = data_line
        label = int(speech_to_text.spice_dict[label])

        num_correct += 1 if speech_to_text.predict_spice(model, data) == label else 0
    
    acc = num_correct / num_avail
    
    print(f'Accuracy: {acc}')

    if (acc > 0.9):
        speech_to_text.save_trained_model(model)



    

            



