import socket
import threading
import pickle
from field import Field
from deck import Deck
from heap import Heap
from settings import WindowParameters, GameConstants

HEADER_SIZE = 10

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()
        self.field = Field()
        self.deck = Deck(Heap().give_chips(Deck.N_CHIPS_MAX_VALUE))

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'Server started on {self.host}:{self.port}')
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'Client {client_address} connected')
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def broadcast(self, message):
        with self.lock:
            for client in self.clients:
                try:
                    message = pickle.dumps(message)
                    message = bytes(f"{len(message):<{HEADER_SIZE}}", 'utf-8') + message
                    client.sendall(message)
                except Exception as e:
                    print(f'Error sending message to client: {e}')
                    self.clients.remove(client)
                    client.close()

    def handle_client(self, client_socket):
        while True:
            try:
                full_message = b""
                new_msg = True
                while True:
                    msg = client_socket.recv(16)
                    if new_msg:
                        print(f"New message length: {msg[:HEADER_SIZE].decode()}")
                        msg_len = int(msg[:HEADER_SIZE])
                        new_msg = False

                    full_message += msg

                    if len(full_message) - HEADER_SIZE == msg_len:
                        print("Full message received")
                        self.handle_message(client_socket, full_message[HEADER_SIZE:])
                        new_msg = True
                        full_message = b""
            except ConnectionResetError:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print('Client disconnected')

    def handle_message(self, client_socket, message):
        data = pickle.loads(message)
        if data['type'] == 'move':
            chip = data['chip']
            cell_indexes = data['cell_indexes']
            print(f"Received move: {chip}, cell indexes: {cell_indexes}")
            self.field.place_chip(chip, cell_indexes)
            update_message = {
                'type': 'update',
                'field': self.field,
                'deck': self.deck
            }
            self.broadcast(update_message)
            print("Broadcasted update to all clients.")

if __name__ == "__main__":
    server = GameServer()
    server.start()
