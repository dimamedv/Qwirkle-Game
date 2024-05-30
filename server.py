import socket
import threading
import pickle

from field import Field
from heap import Heap
from chip import Chip
from settings import WindowParameters, GameConstants


class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

        self.field = Field()
        self.heap = Heap()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f'Сервер запущен на {self.host}:{self.port}')

        while True:
            client_socket, client_address = self.server_socket.accept()

            print(f'Клиент {client_address} подключен')

            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def broadcast(self, message):
        message = len(message).to_bytes(4, 'big') + message

        with self.lock:
            for client in self.clients:
                try:
                    client.sendall(message)
                except Exception as e:
                    print(f'Ошибка отправки сообщения клиенту: {e}')

                    self.clients.remove(client)
                    client.close()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(4096)

                if not message:
                    break

                self.handle_message(client_socket, message)
            except ConnectionResetError:
                break

        client_socket.close()
        self.clients.remove(client_socket)

        print('Клиент отключен')

    def handle_message(self, client_socket, message) -> None:
        buffer = message

        while True:
            if len(buffer) < 4:
                break

            msg_len = int.from_bytes(buffer[:4], 'big')

            if len(buffer) < 4 + msg_len:
                break

            message = buffer[4:4 + msg_len]
            buffer = buffer[4 + msg_len:]
            data = pickle.loads(message)

            if data['type'] == 'move':
                chip = data['chip']
                cell_indexes = data['cell_indexes']

                self.field.place_chip(chip, cell_indexes)

                update_message = pickle.dumps({
                    'type': 'update',
                    'field': self.field
                })

                self.broadcast(update_message)

                print("Отправлено обновление всем клиентам.")
            elif data['type'] == 'give_chips':
                n_chips = data['n_chips']

                given_chips = self.heap.give_chips(n_chips)

                update_message = pickle.dumps({
                    'type': 'get_new_deck',
                    'new_chips': given_chips
                })

                self.broadcast(update_message)
            elif data['type'] == 'exchange_chips':
                returned_chips = data['returned_chips']

                substitute = self.heap.make_an_exchange_of_chips(returned_chips)

                update_message = pickle.dumps({
                    'type': 'update_deck',
                    'substitute': substitute
                })

                self.broadcast(update_message)
            elif data['type'] == 'return_extra_chips':
                self.heap.return_chips(data['extra_chips'])
            elif data['type'] == 'get_heap_state':
                is_empty = self.heap.is_empty()
                n_chips = self.heap.n_chips()

                update_message = pickle.dumps({
                    'type': 'receive_heap_state',
                    'is_heap_empty': is_empty,
                    'n_chips_of_heap': n_chips
                })

                self.send_message_to_client(client_socket, update_message)

                print("отправлено обновление клиенту.")

    def send_message_to_client(self, client_socket, message) -> None:
        message = len(message).to_bytes(4, 'big') + message

        client_socket.sendall(message)


if __name__ == "__main__":
    server = GameServer()

    server.start()
