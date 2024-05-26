import socket
import threading
import pygame
import pickle
import sys
from field import Field
from deck import Deck
from heap import Heap
from chip import Chip
from settings import WindowParameters, GameConstants

class GameClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.field = Field()
        self.deck = Deck(Heap().give_chips(Deck.N_CHIPS_MAX_VALUE))
        self.current_chip = None
        self.current_chip_index = -1
        self.are_sounds_muted = False
        self.is_shift_of_displayed_part_blocked = False
        self.exchanged_chips_indexes = []

        # Инициализация Pygame и микшера перед загрузкой звуков
        pygame.init()
        pygame.mixer.init()

        self.chip_was_put_up_sound = pygame.mixer.Sound("resources/sounds/chip_was_put_up.wav")
        self.shift_of_displayed_part_of_field_sound = pygame.mixer.Sound("resources/sounds/shift_of_displayed_part_of_field.wav")

    def start(self):
        self.client_socket.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages).start()
        self.game_cycle()

    def receive_messages(self):
        buffer = b''
        while True:
            try:
                message = self.client_socket.recv(4096)
                if not message:
                    break
                buffer += message
                while True:
                    if len(buffer) < 4:
                        break
                    msg_len = int.from_bytes(buffer[:4], 'big')
                    if len(buffer) < 4 + msg_len:
                        break
                    message = buffer[4:4 + msg_len]
                    buffer = buffer[4 + msg_len:]
                    self.handle_message(message)
            except ConnectionResetError:
                break

    def handle_message(self, message):
        data = pickle.loads(message)
        if data['type'] == 'update':
            self.field = data['field']

    def send_message(self, message):
        message = len(message).to_bytes(4, 'big') + message
        self.client_socket.sendall(message)

    def draw_field(self, field_for_draw: Field) -> None:
        min_x = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X
        max_x = min_x + WindowParameters.DISPLAYED_PART_OF_FIELD_WIDTH

        min_y = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y
        max_y = min_y + WindowParameters.DISPLAYED_PART_OF_FIELD_HEIGHT

        for x in range(min_x, max_x, WindowParameters.CELL_SIZE):
            for y in range(min_y, max_y, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

                cell_column_index = ((x - min_x) // WindowParameters.CELL_SIZE + field_for_draw.cell_column_index_shift)
                cell_row_index = ((y - min_y) // WindowParameters.CELL_SIZE + field_for_draw.cell_row_index_shift)

                cell_indexes = (cell_row_index, cell_column_index)
                cell_content = field_for_draw.get_content_of_cell(cell_indexes)

                if isinstance(cell_content, Chip):
                    pygame.draw.rect(screen, GameConstants.BLACK_COLOR, rect, WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)
                    cell_content.draw_figure(screen, (x, y), WindowParameters.CELL_SIZE)

                    if cell_indexes == field_for_draw.last_choice:
                        if field_for_draw.n_put_up_chips == 1:
                            chip_border_color = GameConstants.BLUE_COLOR_FOR_CHIP_BORDER
                        elif field_for_draw.is_last_choice_correct():
                            chip_border_color = GameConstants.GREEN_COLOR_FOR_CHIP_BORDER
                        else:
                            chip_border_color = GameConstants.RED_COLOR_FOR_CHIP_BORDER

                        pygame.draw.rect(screen, chip_border_color, rect, WindowParameters.CURRENT_CHIP_BORDER_SIZE)
                else:
                    pygame.draw.rect(screen, GameConstants.BLACK_COLOR, rect, 1)

    def draw_deck(self, deck_for_draw: Deck, current_chip_index: int) -> None:
        y = WindowParameters.DECK_RIGHT_CORNER_Y

        left_corner_x = WindowParameters.DECK_LEFT_CORNER_X
        right_corner_x = left_corner_x + WindowParameters.DECK_WIDTH

        step = WindowParameters.CELL_SIZE + WindowParameters.DECK_DISTANCE_BETWEEN_CHIPS

        chip_index = 0

        for x in range(left_corner_x, right_corner_x, step):
            rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

            chip = deck_for_draw.chip(chip_index)

            if chip is not None:
                pygame.draw.rect(screen, GameConstants.BLACK_COLOR, rect, WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)
                chip.draw_figure(screen, (x, y), WindowParameters.CELL_SIZE)

                if chip_index == current_chip_index:
                    pygame.draw.rect(screen, GameConstants.PURPLE_COLOR_FOR_CHOSEN_DECK_CHIP, rect, WindowParameters.CURRENT_CHIP_BORDER_SIZE)
            else:
                pygame.draw.rect(screen, GameConstants.BLACK_COLOR, rect, WindowParameters.CELL_BORDER_SIZE)

            chip_index += 1

    def is_mouse_on_the_field(self, mouse_pos: tuple[int, int]) -> bool:
        x, y = mouse_pos
        return (WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X <= x <= WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_X) and \
               (WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y <= y <= WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_Y)

    def get_cell_indexes_by_mouse_pos(self, mouse_pos: tuple[int, int], viewed_field: Field) -> tuple[int, int]:
        x, y = mouse_pos
        cell_column_index = (x - WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X) // WindowParameters.CELL_SIZE + viewed_field.cell_column_index_shift
        cell_row_index = (y - WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y) // WindowParameters.CELL_SIZE + viewed_field.cell_row_index_shift
        return cell_row_index, cell_column_index

    def handle_left_click(self, choice_cell_indexes: tuple[int, int], field_for_edit: Field, chip_for_putting_up: Chip) -> bool:
        if not field_for_edit.has_chip_in_this_cell(choice_cell_indexes):
            field_for_edit.place_chip(chip_for_putting_up, choice_cell_indexes)
            field_for_edit.last_choice = choice_cell_indexes
            if field_for_edit.is_last_choice_correct():
                return True
            else:
                field_for_edit.remove_chip(choice_cell_indexes)
                field_for_edit.reset_last_choice()
        return False

    def return_chip_back_to_the_deck(self, chip: Chip, chip_index: int, field: Field, deck: Deck) -> None:
        deck.place_chip(chip, chip_index)

        if not field.has_last_choice_init_value():
            field.remove_chip(field.last_choice)
            field.reset_last_choice()

    def confirm_move(self):
        if not self.are_sounds_muted:
            self.chip_was_put_up_sound.play()
        message = pickle.dumps({
            'type': 'move',
            'chip': self.current_chip,
            'cell_indexes': self.field.last_choice
        })
        self.send_message(message)
        self.current_chip = None
        self.current_chip_index = -1

    def game_cycle(self) -> None:
        global screen

        screen = pygame.display.set_mode((WindowParameters.WIDTH, WindowParameters.HEIGHT))
        pygame.display.set_caption("Квиркл")

        heap = Heap()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.client_socket.close()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_on_the_field(pygame.mouse.get_pos()):
                    cell_indexes = self.get_cell_indexes_by_mouse_pos(pygame.mouse.get_pos(), self.field)
                    cell_content = self.field.get_content_of_cell(cell_indexes)

                    if event.button == 1 and not isinstance(cell_content, Chip) and self.current_chip is not None:
                        self.field_copy = self.field.copy(copy_last_choice=True)
                        if self.handle_left_click(cell_indexes, self.field_copy, self.current_chip):
                            self.deck.remove_chip(self.current_chip_index)
                            self.field = self.field_copy.copy(copy_last_choice=True)
                            self.confirm_move()
                    elif event.button == 3 and self.field.is_last_choice_correct() and cell_indexes == self.field.last_choice:
                        self.field.reset_last_choice()
                        if not self.are_sounds_muted:
                            self.chip_was_put_up_sound.play()
                        self.current_chip = None
                        self.current_chip_index = -1
                elif event.type == pygame.KEYDOWN:
                    if event.key in GameConstants.SIMPLE_ACTIONS_KEYS:
                        match event.key:
                            case pygame.K_b:
                                self.is_shift_of_displayed_part_blocked = not self.is_shift_of_displayed_part_blocked
                            case pygame.K_m:
                                self.are_sounds_muted = not self.are_sounds_muted
                            case pygame.K_e:
                                if self.current_chip_index not in self.exchanged_chips_indexes and self.current_chip is not None:
                                    self.exchanged_chips_indexes.append(self.current_chip_index)
                                    self.current_chip = heap.make_an_exchange_of_chips([self.current_chip])[0]
                                    self.return_chip_back_to_the_deck(self.current_chip, self.current_chip_index, self.field, self.deck)
                    elif event.key in GameConstants.CHOICE_OF_DECK_CHIP_KEYS:
                        chip_index = GameConstants.CHOICE_OF_DECK_CHIP_KEYS.index(event.key)
                        chip = self.deck.chip(chip_index)
                        if chip is not None:
                            if self.current_chip is not None and chip_index != self.current_chip_index:
                                self.return_chip_back_to_the_deck(self.current_chip, self.current_chip_index, self.field, self.deck)
                            self.current_chip = chip
                            self.current_chip_index = chip_index
                    elif not self.is_shift_of_displayed_part_blocked and event.key in GameConstants.SHIFT_OF_DISPLAYED_PART_OF_FIELD_KEYS:
                        match event.key:
                            case pygame.K_w | pygame.K_UP:
                                self.field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_UP)
                            case pygame.K_s | pygame.K_DOWN:
                                self.field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_DOWN)
                            case pygame.K_a | pygame.K_LEFT:
                                self.field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_LEFT)
                            case pygame.K_d | pygame.K_RIGHT:
                                self.field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_RIGHT)
                            case pygame.K_c:
                                self.field.reset_cell_row_index_shift()
                                self.field.reset_cell_column_index_shift()
                        if not self.are_sounds_muted:
                            self.shift_of_displayed_part_of_field_sound.play()

            screen.fill(pygame.Color("white"))
            self.draw_field(self.field)
            self.draw_deck(self.deck, self.current_chip_index)
            pygame.display.flip()

if __name__ == "__main__":
    client = GameClient()
    client.start()
