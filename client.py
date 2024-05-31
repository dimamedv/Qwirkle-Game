import sys

from copy import copy

import socket
import pickle

import threading
import queue

import pygame

from field import Field
from deck import Deck
from chip import Chip
from settings import WindowParameters, GameConstants


class GameClient:
    def __init__(self, host="localhost", port=12345) -> None:
        self.host = host
        self.port = port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.has_right_to_move = False

        self.field = Field()
        self.field_copy = self.field.copy()

        self.current_chip = None
        self.current_chip_index = -1

        self.are_sounds_muted = False
        self.is_shift_of_displayed_part_blocked = False

        self.deck = None

        self.exchanged_chips_indexes = []
        self.indexes_of_chips_to_exchange = []

        self.leaderboard = []
        self.players_queue = []
        self.current_player_name = None

        self.new_chips_indexes = []

        self.necessary_property = []

        self.is_game_over = False

        self.is_exchange_buttons_blocked = False

        self.messages_queue = queue.Queue()

        pygame.init()
        pygame.mixer.init()

        self.chip_was_put_up_sound = pygame.mixer.Sound(
            "resources/sounds/chip_was_put_up.wav")

        self.shift_of_displayed_part_of_field_sound = pygame.mixer.Sound(
            "resources/sounds/shift_of_displayed_part_of_field.wav")

        self.font = pygame.font.Font(
            "resources/fonts/unbounded bold.ttf",
            WindowParameters.FONT_SIZE)

        self.deck_chips_rects = \
            self.get_rects(
                WindowParameters.DECK_MIN_X,
                WindowParameters.DECK_MAX_X,
                WindowParameters.DECK_MIN_Y,
                WindowParameters.DECK_STEP,
                (WindowParameters.CELL_SIZE,
                 WindowParameters.CELL_SIZE))

        self.buttons_rects = \
            self.get_rects(
                WindowParameters.BUTTONS_MIN_X,
                WindowParameters.BUTTONS_MAX_X,
                WindowParameters.BUTTONS_MIN_Y,
                WindowParameters.BUTTONS_STEP,
                (WindowParameters.BUTTON_WIDTH,
                 WindowParameters.CELL_SIZE))

        self.buttons_labels = ["Обмен", "Обмен *", "Ход"]

    def start(self) -> None:
        self.client_socket.connect((self.host, self.port))

        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.send_give_chips_message(Deck.N_CHIPS_MAX_VALUE)

        self.game_cycle()

    def receive_messages(self) -> None:
        buffer = b""

        while True:
            try:
                message = self.client_socket.recv(4096)

                if not message:
                    break

                buffer += message

                while True:
                    if len(buffer) < 4:
                        break

                    msg_len = int.from_bytes(buffer[:4], "big")

                    if len(buffer) < 4 + msg_len:
                        break

                    message = buffer[4:4 + msg_len]
                    buffer = buffer[4 + msg_len:]

                    data = pickle.loads(message)
                    self.messages_queue.put(data)
            except socket.timeout:
                continue
            except ConnectionResetError:
                break

    def handle_message(self, data) -> None:
        match data["type"]:
            case "update_clients":
                self.field = data["field"].copy()

                self.leaderboard = sorted(
                    data["leaderboard"],
                    key=lambda x: x[1],
                    reverse=True)
            case "get_right_to_move":
                self.has_right_to_move = True
            case "get_given_chips":
                given_chips = data["given_chips"]

                if given_chips:
                    if self.deck is None:
                        self.deck = Deck(given_chips)

                        self.send_max_n_of_same_type_chips_message()
                    else:
                        self.new_chips_indexes = self.deck.empty_places_for_chips_indexes

                        extra_chips = self.deck.replenish(given_chips)

                        if not self.deck.is_full:
                            self.new_chips_indexes = \
                                list(set(self.new_chips_indexes) -
                                     set(self.deck.empty_places_for_chips_indexes))

                        self.current_chip = None
                        self.current_chip_index = -1

                        if extra_chips:
                            self.send_return_chips_message(extra_chips)
            case "update_deck":
                substitute = data["substitute"]

                if substitute:
                    if isinstance(substitute, Chip):
                        self.current_chip = substitute

                        self.return_chip_back_to_the_deck()

                        self.exchanged_chips_indexes.append(self.current_chip_index)
                    elif isinstance(substitute, list):
                        n_unexchanged_chips = \
                            (len(self.indexes_of_chips_to_exchange) - len(substitute))

                        if n_unexchanged_chips:
                            self.indexes_of_chips_to_exchange = \
                                self.indexes_of_chips_to_exchange[:-n_unexchanged_chips]

                        self.exchanged_chips_indexes = \
                            list(set(self.exchanged_chips_indexes) |
                                 set(self.indexes_of_chips_to_exchange))

                        if self.indexes_of_chips_to_exchange:
                            self.deck.place_on_places(
                                substitute,
                                self.indexes_of_chips_to_exchange)

                        self.indexes_of_chips_to_exchange = []

                        self.current_chip = None
                        self.current_chip_index = -1
            case "receive_heap_state_for_exchange_of_chip":
                is_heap_empty = data["is_heap_empty"]
                n_chips_of_heap = data["n_chips_of_heap"]

                if (is_heap_empty is not None and not is_heap_empty and
                        len(self.exchanged_chips_indexes) < n_chips_of_heap and
                        self.current_chip_index not in self.exchanged_chips_indexes and
                        self.current_chip is not None and
                        self.field.has_last_choice_init_value()):
                    self.send_exchange_of_chips_message([self.current_chip])
            case "get_leaderboard_and_players_queue":
                self.leaderboard = sorted(
                    data["leaderboard"],
                    key=lambda x: x[1],
                    reverse=True)

                self.players_queue = data["players_queue"]

                self.current_player_name = data["current_player_name"]
            case "get_current_player_name":
                self.current_player_name = data["current_player_name"]
            case "game_over":
                self.leaderboard = sorted(
                    data["leaderboard"],
                    key=lambda x: x[1],
                    reverse=True)

    def send_message(self, message) -> None:
        message = len(message).to_bytes(4, "big") + message

        self.client_socket.sendall(message)

    def send_give_chips_message(self, n_chips) -> None:
        message = pickle.dumps(
            {"type": "give_chips",
             "n_chips": n_chips
             })

        self.send_message(message)

    def send_exchange_of_chips_message(self, returned_chips) -> None:
        message = pickle.dumps(
            {"type": "exchange_chips",
             "returned_chips": returned_chips
             })

        self.send_message(message)

    def send_return_chips_message(
            self,
            returned_chips: list[Chip]) -> None:
        message = pickle.dumps(
            {"type": "return_extra_chips",
             "returned_chips": returned_chips
             })

        self.send_message(message)

    def send_place_chip_message(
            self,
            current_chip: Chip,
            cell_indexes: tuple[int, int],
            points: int) -> None:
        message = pickle.dumps({
            "type": "place_chip",
            "chip": current_chip,
            "cell_indexes": cell_indexes,
            "points": points,
            "cell_row_index_shift": self.field.cell_row_index_shift,
            "cell_column_index_shift": self.field.cell_column_index_shift,
            "min_max_cell_indexes": self.field.min_max_cell_indexes
        })

        self.send_message(message)

    def send_make_an_exchange_of_chip_message(self) -> None:
        message = pickle.dumps({
            "type": "make_an_exchange_of_chip"
        })

        self.send_message(message)

    def send_make_an_exchange_of_all_unexchanged_chips_message(self) -> None:
        message = pickle.dumps({
            "type": "make_an_exchange_of_all_unexchanged_chips"
        })

        self.send_message(message)

    def send_complete_the_move_message(self) -> None:
        message = pickle.dumps({
            "type": "complete_the_move"
        })

        self.send_message(message)

    def send_max_n_of_same_type_chips_message(self) -> None:
        message = pickle.dumps({
            "type": "get_max_n_of_same_type_chips",

            "max_n_of_same_type_chips":
                self.deck.max_n_of_same_by_color_or_figure_chips
        })

        self.send_message(message)

    def send_useless_deck_message(self) -> None:
        message = pickle.dumps({
            "type": "useless_deck",
        })

        self.send_message(message)

    def make_an_exchange_of_all_unexchanged_chips(self) -> None:
        self.indexes_of_chips_to_exchange = \
            list(set(self.deck.non_empty_places_for_chips_indexes) -
                 set(self.exchanged_chips_indexes))

        deck_returned_content = \
            copy(self.deck.content_on_places(self.indexes_of_chips_to_exchange))

        self.send_exchange_of_chips_message(deck_returned_content)

    def draw_field(
            self,
            field_for_draw: Field,
            is_correct_next_chip: bool) -> None:
        min_x = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X
        max_x = min_x + WindowParameters.DISPLAYED_PART_OF_FIELD_WIDTH
        min_y = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y
        max_y = min_y + WindowParameters.DISPLAYED_PART_OF_FIELD_HEIGHT

        for x in range(min_x, max_x, WindowParameters.CELL_SIZE):
            for y in range(min_y, max_y, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(
                    x,
                    y,
                    WindowParameters.CELL_SIZE,
                    WindowParameters.CELL_SIZE)

                cell_column_index = \
                    ((x - min_x) //
                     WindowParameters.CELL_SIZE +
                     field_for_draw.cell_column_index_shift)

                cell_row_index = \
                    ((y - min_y) //
                     WindowParameters.CELL_SIZE +
                     field_for_draw.cell_row_index_shift)

                cell_indexes = (cell_row_index, cell_column_index)
                cell_content = field_for_draw.get_content_of_cell(cell_indexes)

                if isinstance(cell_content, Chip):
                    pygame.draw.rect(
                        screen,
                        GameConstants.BLACK_COLOR,
                        rect,
                        WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)

                    cell_content.draw_figure(
                        screen,
                        (x, y),
                        WindowParameters.CELL_SIZE)

                    if cell_indexes == field_for_draw.last_choice:
                        if (field_for_draw.n_put_up_chips == 1 and
                                is_correct_next_chip):
                            chip_border_color = GameConstants.GRAY_COLOR
                        elif (field_for_draw.is_last_choice_correct() and
                              is_correct_next_chip):
                            chip_border_color = GameConstants.GREEN_COLOR
                        else:
                            chip_border_color = GameConstants.RED_COLOR

                        pygame.draw.rect(
                            screen,
                            chip_border_color,
                            rect,
                            WindowParameters.CURRENT_CHIP_BORDER_SIZE)
                else:
                    pygame.draw.rect(
                        screen,
                        GameConstants.BLACK_COLOR,
                        rect,
                        WindowParameters.CELL_BORDER_SIZE)

    def draw_deck(
            self,
            first_chips: list[Chip] = None) -> None:
        chip_index = 0

        for rect in self.deck_chips_rects:
            chip = self.deck.chip(chip_index)

            if chip is not None:
                pygame.draw.rect(
                    screen,
                    GameConstants.BLACK_COLOR,
                    rect,
                    WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)

                chip.draw_figure(
                    screen,
                    (rect.x, rect.y),
                    WindowParameters.CELL_SIZE)

                border_color = GameConstants.BLACK_COLOR

                if chip_index == self.current_chip_index:
                    border_color = GameConstants.PURPLE_COLOR
                elif first_chips is not None and chip in first_chips:
                    border_color = GameConstants.GOLD_COLOR

                pygame.draw.rect(
                    screen,
                    border_color,
                    rect,
                    WindowParameters.CURRENT_CHIP_BORDER_SIZE)

                is_index_of_exchanged_chip = chip_index in self.exchanged_chips_indexes
                is_index_of_new_chip = chip_index in self.new_chips_indexes

                if is_index_of_exchanged_chip or is_index_of_new_chip:
                    line_color = GameConstants.WHITE_COLOR

                    if is_index_of_exchanged_chip:
                        line_color = GameConstants.RED_COLOR
                    elif is_index_of_new_chip:
                        line_color = GameConstants.BLUE_COLOR

                    line_min_x = rect.x
                    line_max_x = rect.x + WindowParameters.CELL_SIZE

                    line_y = (rect.y + WindowParameters.CELL_SIZE +
                              WindowParameters.DECK_DISTANCE_BETWEEN_CHIPS)

                    pygame.draw.line(
                        screen,
                        line_color,
                        (line_min_x, line_y),
                        (line_max_x, line_y),
                        WindowParameters.CURRENT_CHIP_BORDER_SIZE)
            else:
                pygame.draw.rect(
                    screen,
                    GameConstants.BLACK_COLOR,
                    rect,
                    WindowParameters.CELL_BORDER_SIZE)

            chip_index += 1

    def draw_label(
            self,
            rect: pygame.Rect,
            text: str,
            text_color: pygame.Color,
            background_color: pygame.Color = GameConstants.WHITE_COLOR,
            position=None) -> None:
        pygame.draw.rect(
            screen,
            GameConstants.WHITE_COLOR,
            rect,
            WindowParameters.CELL_BORDER_SIZE)

        text_surface = self.font.render(
            text,
            True,
            text_color,
            background_color)

        if position is not None:
            text_rect = text_surface.get_rect(center=position)

            screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, rect)

    @staticmethod
    def get_rects(
            left_corner_x: int,
            right_corner_x: int,
            y: int,
            step: int,
            rect_sizes: tuple[int, int]) -> list[pygame.Rect]:
        rects = []

        for x in range(left_corner_x, right_corner_x, step):
            rect = pygame.Rect(x, y, rect_sizes[0], rect_sizes[1])

            rects.append(rect)

        return rects

    def draw_buttons(
            self) -> None:
        i = 0
        for rect in self.buttons_rects:
            if self.has_right_to_move:
                button_color = GameConstants.BLACK_COLOR
                label_background_color = button_color
            else:
                button_color = GameConstants.GRAY_COLOR
                label_background_color = button_color

            if (i < (WindowParameters.N_BUTTONS - 1) and
                    self.is_exchange_buttons_blocked):
                button_color = GameConstants.GRAY_COLOR
                label_background_color = button_color

            pygame.draw.rect(
                screen,
                button_color,
                rect,
                WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)

            self.draw_label(
                rect,
                self.buttons_labels[i],
                GameConstants.WHITE_COLOR,
                label_background_color,
                rect.center)

            i += 1

    def draw_info(
            self,
            n_laid_out_chips: int) -> None:
        if self.is_game_over:
            text = "Конец игры"
        elif (self.field.has_last_choice_init_value() and
              n_laid_out_chips == 0 and
              self.has_right_to_move and
              self.field.is_deck_useless(
                  self.deck.content
                  if not self.necessary_property
                  else self.deck.get_chips_by_property_value(
                      next(filter(lambda x: x is not None,
                                  self.necessary_property),
                           None)
                  ))):
            text = "Ваша колода бесполезна"

            self.send_useless_deck_message()
        else:
            text = ""

        self.draw_label(
            pygame.Rect(
                WindowParameters.IS_USELESS_DECK_LABEL_MIN_X,
                WindowParameters.IS_USELESS_DECK_LABEL_MIN_Y,
                WindowParameters.IS_USELESS_DECK_LABEL_WIDTH,
                WindowParameters.IS_USELESS_DECK_LABEL_HEIGHT),
            text,
            GameConstants.RED_COLOR)

        if self.has_right_to_move:
            text = "Сейчас ваш ход"
        else:
            text = "Сейчас ход другого игрока"

        self.draw_label(
            pygame.Rect(
                WindowParameters.HAS_PLAYER_RIGHT_TO_MOVE_LABEL_MIN_X,
                WindowParameters.HAS_PLAYER_RIGHT_TO_MOVE_LABEL_MIN_Y,
                WindowParameters.HAS_PLAYER_RIGHT_TO_MOVE_LABEL_WIDTH,
                WindowParameters.HAS_PLAYER_RIGHT_TO_MOVE_LABEL_HEIGHT),
            text,
            GameConstants.BLACK_COLOR)

        y = WindowParameters.LEADERBOARD_MIN_Y

        self.leaderboard.insert(0, ["Рейтинг:", ""])

        i = 0
        for row in self.leaderboard:
            if i == 0:
                number = ""
                hyphen = ""
            else:
                number = str(i) + ". "
                hyphen = "  —  "

            self.draw_label(
                pygame.Rect(
                    WindowParameters.LEADERBOARD_MIN_X,
                    y,
                    WindowParameters.LEADERBOARD_ROW_RECT_WIDTH,
                    WindowParameters.LEADERBOARD_ROW_RECT_HEIGHT),
                number + row[0] + hyphen + str(row[1]),
                GameConstants.BLACK_COLOR)

            y += WindowParameters.LEADERBOARD_ROW_RECT_HEIGHT

            i += 1

        self.leaderboard.pop(0)

        y = WindowParameters.PLAYERS_QUEUE_MIN_Y

        self.players_queue.insert(0, "Очередь:")

        i = 0
        for row in self.players_queue:
            if i == 0:
                number = ""
            else:
                number = str(i) + ". "

            if i == 0 or row == self.current_player_name:
                text_color = GameConstants.BLACK_COLOR
            else:
                text_color = GameConstants.GRAY_COLOR

            self.draw_label(
                pygame.Rect(
                    WindowParameters.PLAYERS_QUEUE_MIN_X,
                    y,
                    WindowParameters.PLAYERS_QUEUE_ROW_RECT_WIDTH,
                    WindowParameters.PLAYERS_QUEUE_ROW_RECT_WIDTH),
                number + row,
                text_color)

            y += WindowParameters.LEADERBOARD_ROW_RECT_HEIGHT

            i += 1

        self.players_queue.pop(0)

    def is_mouse_on_the_field(
            self,
            mouse_pos: tuple[int, int]) -> bool:
        x, y = mouse_pos

        return \
            ((WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X
              <= x
              <= WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_X) and
             (WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y
              <= y
              <= WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_Y))

    def get_cell_indexes_by_mouse_pos(
            self,
            mouse_pos: tuple[int, int],
            viewed_field: Field) -> tuple[int, int]:
        x, y = mouse_pos

        cell_column_index = \
            ((x - WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X) //
             WindowParameters.CELL_SIZE +
             viewed_field.cell_column_index_shift)

        cell_row_index = \
            ((y - WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y) //
             WindowParameters.CELL_SIZE +
             viewed_field.cell_row_index_shift)

        return cell_row_index, cell_column_index

    def handle_left_click(
            self,
            choice_cell_indexes: tuple[int, int]) -> None:
        if not self.field_copy.has_chip_in_this_cell(choice_cell_indexes):
            self.field_copy.place_chip(self.current_chip, choice_cell_indexes)

        if not self.field_copy.has_last_choice_init_value() and \
                choice_cell_indexes != self.field_copy.last_choice:
            self.field_copy.remove_chip(self.field_copy.last_choice)

        self.field_copy.last_choice = choice_cell_indexes

    def return_chip_back_to_the_deck(self) -> None:
        self.deck.place_chip(
            self.current_chip,
            self.current_chip_index)

        if not self.field.has_last_choice_init_value():
            self.field.remove_chip(self.field.last_choice)

            self.field.reset_last_choice()

    def update_current_chip_parameters(
            self,
            certain_value: object,
            container: list | tuple) -> None:
        chip_index = container.index(certain_value)
        chip = self.deck.chip(chip_index)

        if chip is not None:
            if (self.current_chip is not None and
                    chip_index != self.current_chip_index):
                self.return_chip_back_to_the_deck()

            self.current_chip = chip
            self.current_chip_index = chip_index

    def game_cycle(self) -> None:
        global screen

        screen = \
            pygame.display.set_mode(
                (WindowParameters.WIDTH,
                 WindowParameters.HEIGHT))

        pygame.display.set_caption("Квиркл")

        type_of_actions = None

        first_chip = None

        n_put_up_chips = 0

        is_next_chip_correct = True

        while True:
            while not self.messages_queue.empty():
                data = self.messages_queue.get()

                self.handle_message(data)

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()

                        self.client_socket.close()

                        sys.exit()
                    case pygame.MOUSEBUTTONDOWN:
                        if (type_of_actions in (None, "placing_of_chips") and
                                self.is_mouse_on_the_field(pygame.mouse.get_pos())):
                            cell_indexes = \
                                self.get_cell_indexes_by_mouse_pos(
                                    pygame.mouse.get_pos(),
                                    self.field)

                            cell_content = \
                                self.field.get_content_of_cell(cell_indexes)

                            if n_put_up_chips == 1:
                                is_next_chip_correct = \
                                    ((self.current_chip.figure ==
                                      first_chip.figure) !=
                                     (self.current_chip.color_of_figure ==
                                      first_chip.color_of_figure))
                            elif n_put_up_chips > 1:
                                if self.necessary_property[0] is not None:
                                    is_next_chip_correct = \
                                        self.current_chip.figure == self.necessary_property[0]
                                elif self.necessary_property[1] is not None:
                                    is_next_chip_correct = \
                                        self.current_chip.color_of_figure == \
                                        self.necessary_property[1]

                            if self.has_right_to_move:
                                if (event.button == 1 and
                                        not isinstance(cell_content, Chip) and
                                        self.current_chip is not None):
                                    self.field_copy = self.field.copy(copy_last_choice=True)

                                    self.deck.remove_chip(self.current_chip_index)

                                    self.handle_left_click(cell_indexes)

                                    self.field = self.field_copy.copy(copy_last_choice=True)
                                elif (event.button == 3 and
                                      self.field.is_last_choice_correct() and
                                      cell_indexes == self.field.last_choice and
                                      is_next_chip_correct):
                                    if type_of_actions is None:
                                        type_of_actions = "placing_of_chips"

                                    if self.field.has_only_one_chip():
                                        choice_points = 1
                                    else:
                                        choice_points = \
                                            self.field.is_last_choice_correct_in_the_context_of_chips_lines(
                                                cell_indexes)[1]

                                    if n_put_up_chips == 0:
                                        first_chip = self.current_chip
                                    elif n_put_up_chips == 1:
                                        self.necessary_property.append(
                                            first_chip.figure
                                            if first_chip.figure == self.current_chip.figure
                                            else None)

                                        self.necessary_property.append(
                                            first_chip.color_of_figure
                                            if first_chip.color_of_figure == self.current_chip.color_of_figure
                                            else None)

                                    self.field.reset_last_choice()

                                    if not self.are_sounds_muted:
                                        self.chip_was_put_up_sound.play()

                                    current_chip_copy = copy(self.current_chip)

                                    self.current_chip = None
                                    self.current_chip_index = -1

                                    self.new_chips_indexes = []

                                    n_put_up_chips += 1

                                    self.is_exchange_buttons_blocked = True

                                    self.send_place_chip_message(
                                        current_chip_copy,
                                        cell_indexes,
                                        choice_points)
                        elif self.has_right_to_move:
                            deck_chips_mouse_choice_checks = \
                                [rect.collidepoint(pygame.mouse.get_pos())
                                 for rect in self.deck_chips_rects]

                            if (True in deck_chips_mouse_choice_checks and
                                    event.button == 1):
                                self.update_current_chip_parameters(
                                    True,
                                    deck_chips_mouse_choice_checks)
                            elif self.buttons_rects[0].collidepoint(
                                    pygame.mouse.get_pos()):
                                if (self.has_right_to_move and
                                        type_of_actions in (None, "exchange_of_chips")
                                        and self.current_chip is not None):
                                    if type_of_actions is None:
                                        type_of_actions = "exchange_of_chips"

                                    self.send_make_an_exchange_of_chip_message()
                            elif (self.buttons_rects[1].collidepoint(
                                    pygame.mouse.get_pos())):
                                if (self.has_right_to_move and
                                        type_of_actions in (None, "exchange_of_chips") and
                                        not self.deck.is_empty and
                                        self.field.has_last_choice_init_value()):
                                    if type_of_actions is None:
                                        type_of_actions = "exchange_of_chips"

                                    self.make_an_exchange_of_all_unexchanged_chips()
                            elif (self.buttons_rects[2].collidepoint(
                                    pygame.mouse.get_pos())):
                                if (self.has_right_to_move and
                                        self.field.has_last_choice_init_value()):
                                    self.exchanged_chips_indexes = []

                                    self.has_right_to_move = False

                                    type_of_actions = None

                                    self.necessary_property = []

                                    first_chip = None

                                    n_put_up_chips = 0

                                    is_next_chip_correct = True

                                    self.is_exchange_buttons_blocked = False

                                    self.send_complete_the_move_message()
                    case pygame.KEYDOWN:
                        if event.key in GameConstants.SIMPLE_ACTIONS_KEYS:
                            match event.key:
                                case pygame.K_b:
                                    self.is_shift_of_displayed_part_blocked = \
                                        not self.is_shift_of_displayed_part_blocked
                                case pygame.K_m:
                                    self.are_sounds_muted = not self.are_sounds_muted
                                case pygame.K_e:
                                    if (self.has_right_to_move and
                                            type_of_actions in (None, "exchange_of_chips")
                                            and self.current_chip is not None):
                                        if type_of_actions is None:
                                            type_of_actions = "exchange_of_chips"

                                        self.send_make_an_exchange_of_chip_message()
                                case pygame.K_r:
                                    if (self.has_right_to_move and
                                            type_of_actions in (None, "exchange_of_chips") and
                                            not self.deck.is_empty and
                                            self.field.has_last_choice_init_value()):
                                        if type_of_actions is None:
                                            type_of_actions = "exchange_of_chips"

                                        self.make_an_exchange_of_all_unexchanged_chips()
                                case pygame.K_f:
                                    if (self.has_right_to_move and
                                            self.field.has_last_choice_init_value()):
                                        self.exchanged_chips_indexes = []

                                        self.has_right_to_move = False

                                        self.send_complete_the_move_message()

                                        type_of_actions = None

                                        self.necessary_property = []

                                        first_chip = None

                                        n_put_up_chips = 0

                                        is_next_chip_correct = True

                                        self.is_exchange_buttons_blocked = False
                                case pygame.K_g:
                                    if not self.field.has_last_choice_init_value():
                                        self.return_chip_back_to_the_deck()
                        elif (self.has_right_to_move and
                              event.key in GameConstants.CHOICE_OF_DECK_CHIP_KEYS):
                            self.update_current_chip_parameters(
                                event.key,
                                GameConstants.CHOICE_OF_DECK_CHIP_KEYS)
                        elif (not self.is_shift_of_displayed_part_blocked and
                              event.key in GameConstants.SHIFT_OF_DISPLAYED_PART_OF_FIELD_KEYS):
                            match event.key:
                                case pygame.K_w | pygame.K_UP:
                                    self.field.shift_displayed_part(
                                        Field.SHIFT_DISPLAYED_PART_UP)
                                case pygame.K_s | pygame.K_DOWN:
                                    self.field.shift_displayed_part(
                                        Field.SHIFT_DISPLAYED_PART_DOWN)
                                case pygame.K_a | pygame.K_LEFT:
                                    self.field.shift_displayed_part(
                                        Field.SHIFT_DISPLAYED_PART_LEFT)
                                case pygame.K_d | pygame.K_RIGHT:
                                    self.field.shift_displayed_part(
                                        Field.SHIFT_DISPLAYED_PART_RIGHT)
                                case pygame.K_c:
                                    self.field.reset_cell_row_index_shift()
                                    self.field.reset_cell_column_index_shift()
                            if not self.are_sounds_muted:
                                self.shift_of_displayed_part_of_field_sound.play()

            screen.fill(GameConstants.WHITE_COLOR)

            self.draw_field(self.field, is_next_chip_correct)

            self.draw_deck()

            self.draw_buttons()

            self.draw_info(n_put_up_chips)

            pygame.display.flip()


if __name__ == "__main__":
    client = GameClient()

    client.start()
