import torch
import numpy as np
import os

class SpeechBuffer:
    def __init__(self, buffer_length, input_length):
        self.buffer_length = buffer_length
        self.buffer = torch.zeros(buffer_length, dtype=torch.int32)

        self.input_length = input_length
        self.end_length = self.buffer_length-self.input_length
        self.current_pointer = 0

        self.buffer_valid = False
        self.buffer_valid_switch = 0
    
    def update_buffer(self, data):
        data = torch.IntTensor(data)

        range = torch.max(data).item() - torch.min(data).item()

        if (range > 750): 
            self.buffer_valid_switch = 1
        elif (range < 200 and self.buffer_valid_switch == 1): 
            self.buffer_valid_switch = 0
            self.buffer_valid = True

        if (self.current_pointer == self.buffer_length):
            self.buffer = torch.roll(self.buffer, -self.input_length, 0)
            self.buffer[(-self.input_length):] = data
        else:
            self.buffer[self.current_pointer:(self.current_pointer + self.input_length)] = torch.IntTensor(data)
            self.current_pointer += self.input_length
    
    def get_buffer_valid(self):
        value = self.buffer_valid
        self.buffer_valid = False
        return value
    
def save_buffer(buffer, name = 'test.wav'):
    np.write(name, 9600, buffer.numpy())

def load_buffer(SPICE_NAME):
    training_buffers = []
    data_dir_path = f'./RecordingSamples/{SPICE_NAME}'
    num_files = os.listdir(data_dir_path)

    for i in range(int(len(num_files) / 2)):
        tensor_input = torch.unsqueeze(torch.unsqueeze(torch.from_numpy(np.loadtxt(f'{data_dir_path}/Recording{i}.txt', dtype=np.float)), 0), 0)
        tensor_input = tensor_input.type(torch.FloatTensor)
        training_buffers.append((tensor_input, SPICE_NAME))
    
    return training_buffers




