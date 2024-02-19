import json
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.server_address = ('localhost', 5000)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.server_address)

    def run(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            data_dict = json.loads(data.decode())
            self.process_data(data_dict)

    def process_data(self, data_dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        data_to_write = {
            timestamp: data_dict
        }
        with open('storage/data.json', 'a') as file:
            json.dump(data_to_write, file, indent=2)  # Ustawienie wcięć na 2 dla czytelniejszego formatu
            file.write('\n')

