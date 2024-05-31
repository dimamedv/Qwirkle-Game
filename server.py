import socket
import threading
import pickle

from field import Field
from heap import Heap
from deck import Deck
from chip import Chip
from settings import WindowParameters, GameConstants


class GameServer:
    def __init__(
            self,
            host="localhost",
            port=12345) -> None:
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []
        self.lock = threading.Lock()

        self.players_points = []

        self.players_with_useless_decks = []

        self.first_player = None
        self.last_player = None
        self.last_player_index = -1

        self.current_player_index = -1

        self.field = Field()
        self.heap = Heap()

    def start(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"сервер запущен на {self.host}:{self.port}")

        i = 1
        while True:
            client_socket, client_address = self.server_socket.accept()

            print(f"клиент {client_address} подключен")

            self.players_points.append([f"player_{i}", 0])
            self.clients.append([client_socket, self.players_points[-1][0]])

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

            i += 1

    def broadcast(self, message):
        message = len(message).to_bytes(4, "big") + message

        with self.lock:
            for client in self.clients:
                try:
                    client[0].sendall(message)
                except Exception as e:
                    print(f"ошибка отправки сообщения клиенту: {e}")

                    self.clients.remove(client)
                    client[0].close()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(4096)

                if not message:
                    break

                client = next((item for item in self.clients if item[0] == client_socket), None)

                self.handle_message(client, message)
            except ConnectionResetError:
                break

        client_socket.close()
        self.clients.remove(client_socket)

        print("клиент отключен.")

    def handle_message(
            self,
            client,
            message) -> None:
        buffer = message

        while True:
            if len(buffer) < 4:
                break

            msg_len = int.from_bytes(buffer[:4], "big")

            if len(buffer) < 4 + msg_len:
                break

            message = buffer[4:4 + msg_len]
            buffer = buffer[4 + msg_len:]
            data = pickle.loads(message)

            match data["type"]:
                case "place_chip":
                    chip = data["chip"]
                    cell_indexes = data["cell_indexes"]
                    points = data["points"]
                    cell_row_index_shift = data["cell_row_index_shift"]
                    cell_column_index_shift = data["cell_column_index_shift"]
                    min_max_cell_indexes = data["min_max_cell_indexes"]

                    self.field.cell_row_index_shift = cell_row_index_shift
                    self.field.cell_column_index_shift = cell_column_index_shift

                    self.field.set_min_max_cell_indexes(min_max_cell_indexes)
                    self.field.place_chip(chip, cell_indexes)

                    self.players_points[self.current_player_index][1] += points

                    self.last_player = client
                    self.last_player_index = self.current_player_index

                    client_message = pickle.dumps({
                        "type": "update_clients",
                        "field": self.field,
                        "leaderboard": self.players_points
                    })

                    self.broadcast(client_message)
                case "give_chips":
                    n_chips = data["n_chips"]

                    given_chips = self.heap.give_chips(n_chips)

                    client_message = pickle.dumps({
                        "type": "get_given_chips",
                        "given_chips": given_chips
                    })

                    self.send_message_to_client(client[0], client_message)
                case "exchange_chips":
                    returned_chips = data["returned_chips"]

                    substitute = self.heap.make_an_exchange_of_chips(returned_chips)

                    client_message = pickle.dumps({
                        "type": "update_deck",
                        "substitute": substitute
                    })

                    self.send_message_to_client(client[0], client_message)
                case "return_chips":
                    self.heap.return_chips(data["returned_chips"])
                case "make_an_exchange_of_chip":
                    is_empty = self.heap.is_empty()
                    n_chips = self.heap.n_chips()

                    client_message = pickle.dumps({
                        "type": "receive_heap_state_for_exchange_of_chip",
                        "is_heap_empty": is_empty,
                        "n_chips_of_heap": n_chips
                    })

                    self.send_message_to_client(client[0], client_message)
                case "complete_the_move":
                    given_chips = self.heap.give_chips(Deck.N_CHIPS_MAX_VALUE)

                    client_message = pickle.dumps({
                        "type": "get_given_chips",
                        "given_chips": given_chips
                    })

                    self.send_message_to_client(client[0], client_message)

                    self.current_player_index += 1

                    if self.current_player_index == len(self.clients):
                        self.current_player_index = 0

                    client_message = pickle.dumps({
                        "type": "get_current_player_name",
                        "current_player_name": self.clients[self.current_player_index][1]
                    })

                    self.broadcast(client_message)

                    self.give_right_to_move(self.clients[self.current_player_index])
                case "get_max_n_of_same_type_chips":
                    max_n_of_same_type_chips = data["max_n_of_same_type_chips"]

                    if (self.first_player is None or
                            self.first_player[2] < max_n_of_same_type_chips):
                        self.first_player = \
                            (*client, max_n_of_same_type_chips)

                        player_index = self.clients.index(client)

                        if self.clients:
                            self.clients.pop(player_index)
                            self.clients.insert(0, client)

                        self.current_player_index = 0

                        self.give_right_to_move(client)

                    players_queue = [item[1] for item in self.clients]

                    client_message = pickle.dumps({
                        "type": "get_leaderboard_and_players_queue",
                        "leaderboard": self.players_points,
                        "players_queue": players_queue,
                        "current_player_name": players_queue[0]
                    })

                    self.broadcast(client_message)

                    self.send_message_to_client(client[0], client_message)
                case "give_heap_state":
                    is_empty = self.heap.is_empty()
                    n_chips = self.heap.n_chips()

                    client_message = pickle.dumps({
                        "type": "get_heap_state",
                        "is_heap_empty": is_empty,
                        "n_chips_of_heap": n_chips
                    })

                    self.send_message_to_client(client[0], client_message)
                case "useless_deck":
                    if self.heap.is_empty():
                        self.players_with_useless_decks.append(client)

                        if len(self.players_with_useless_decks) == len(client):
                            self.players_points[self.last_player_index][1] += 6

                            client_message = pickle.dumps({
                                "type": "game_over",
                                "leaderboard": self.players_points
                            })

                            self.broadcast(client_message)

    def give_right_to_move(
            self,
            client) -> None:
        self.send_message_to_client(
            client[0],
            pickle.dumps({
                "type": "get_right_to_move"
            }))

    def send_message_to_client(
            self,
            client_socket,
            message) -> None:
        message = len(message).to_bytes(4, "big") + message

        client_socket.sendall(message)


if __name__ == "__main__":
    server = GameServer()

    server.start()
