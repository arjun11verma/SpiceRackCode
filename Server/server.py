from microphone_socket import MicrophoneSocket
from speech_buffering import SpeechBuffer
import speech_to_text
from matplotlib import pyplot as plt
from time import time
import numpy as np
import os

def collect_spice_data(spice_name):
    PACKET_SIZE_INT = 8
    NUM_PACKETS_PER_SECOND = 16
    INPUT_TENSOR_LENGTH = PACKET_SIZE_INT * NUM_PACKETS_PER_SECOND

    socket = MicrophoneSocket("0.0.0.0", 4209, "192.168.174.91", 4210, PACKET_SIZE_INT)
    speech_buffer = SpeechBuffer(INPUT_TENSOR_LENGTH, PACKET_SIZE_INT) # ideal length at baud 9600 is 8872
    display_buffer = []

    SPICE_NAME = spice_name

    for i in range(4000):
        data = socket.read_recent_data()
        if (data != None): speech_buffer.update_buffer(data)
        if (speech_buffer.get_buffer_valid()):
            display_buffer.append(speech_buffer.buffer)
            print("Buffer valid!")
    
    print("Recording done!!!")

    save_buffer_name = f'./RecordingSamples/{SPICE_NAME}'

    for j in range(len(display_buffer)):
        np_buffer = display_buffer[j].numpy()
        plt.plot(np_buffer)
        plt.savefig(f'{save_buffer_name}/Recording{j}Plot')
        np.savetxt(f'{save_buffer_name}/Recording{j}.txt', np_buffer)
        plt.clf()

def main():
    PACKET_SIZE_INT = 8
    NUM_PACKETS_PER_SECOND = 16
    INPUT_TENSOR_LENGTH = PACKET_SIZE_INT * NUM_PACKETS_PER_SECOND

    socket = MicrophoneSocket("0.0.0.0", 4209, "192.168.174.91", 4210, PACKET_SIZE_INT)
    speech_buffer = SpeechBuffer(INPUT_TENSOR_LENGTH, PACKET_SIZE_INT) # ideal length at baud 9600 is 8872

    spice_model = speech_to_text.load_model(INPUT_TENSOR_LENGTH, NUM_CLASSES=8)

    for i in range(4000):
        data = socket.read_recent_data()
        if (data != None): speech_buffer.update_buffer(data)

        if (speech_buffer.get_buffer_valid()):
            prediction = speech_to_text.predict_spice(spice_model, speech_buffer.buffer)
            socket.send_spice_data(prediction)


    

if __name__ == "__main__":
    main()
