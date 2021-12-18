import socket
import struct

class MicrophoneSocket:
    def __init__(self, SERVER_IP, SERVER_PORT, CLIENT_IP, CLIENT_PORT, buffer_size_int):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.CLIENT_IP = CLIENT_IP
        self.CLIENT_PORT = CLIENT_PORT
        self.buffer_size_int = buffer_size_int
        self.buffer_size_bytes = buffer_size_int * 4
        self.unpack_string = '<' + ''.join(['i' for a in range(self.buffer_size_int)])

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((SERVER_IP, SERVER_PORT)) # listening on server IP at given port
        print(f'Listening on {SERVER_IP}...')

        self.tcp_socket.listen()
        self.tcp_socket, addr = self.tcp_socket.accept()

        print(f'Found socket at address {addr}')
    
    def read_recent_data(self):
        data = self.tcp_socket.recv(self.buffer_size_bytes)
        if (len(data) == self.buffer_size_bytes): return struct.unpack(self.unpack_string, data)
        else: return None
    
    def omit_initial_buffers(self):
        self.tcp_socket.recv(self.buffer_size_bytes)
    
    def send_spice_data(self, data):
        self.tcp_socket.send(data.to_bytes(1, 'little'))