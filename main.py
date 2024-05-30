from validators import *
from field import Field
from chip import Chip
from heap import Heap
from deck import Deck

import sys
import enum

import pygame

from copy import copy


# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    CELL_SIZE = 50

    HALF_OF_CELL_SIZE = CELL_SIZE // 2

    DISPLAYED_PART_OF_FIELD_WIDTH = \
        (CELL_SIZE *
         Field.DISPLAYED_PART_N_CELLS_IN_WIDTH)

    DISPLAYED_PART_OF_FIELD_HEIGHT = \
        (CELL_SIZE *
         Field.DISPLAYED_PART_N_CELLS_IN_HEIGHT)

    DISPLAYED_PART_OF_FIELD_MIN_X = \
        HALF_OF_CELL_SIZE

    DISPLAYED_PART_OF_FIELD_MIN_Y = \
        DISPLAYED_PART_OF_FIELD_MIN_X

    DISPLAYED_PART_OF_FIELD_MAX_X = \
        (DISPLAYED_PART_OF_FIELD_MIN_X +
         DISPLAYED_PART_OF_FIELD_WIDTH)

    DISPLAYED_PART_OF_FIELD_MAX_Y = \
        (DISPLAYED_PART_OF_FIELD_MIN_Y +
         DISPLAYED_PART_OF_FIELD_HEIGHT)

    LOWER_PANEL_HEIGHT = 150

    DECK_MIN_X = HALF_OF_CELL_SIZE

    DECK_MIN_Y = \
        (DISPLAYED_PART_OF_FIELD_HEIGHT +
         2 * HALF_OF_CELL_SIZE)

    DECK_DISTANCE_BETWEEN_CHIPS = 10

    DECK_WIDTH = \
        (Deck.N_CHIPS_MAX_VALUE * CELL_SIZE +
         (Deck.N_CHIPS_MAX_VALUE - 1) * DECK_DISTANCE_BETWEEN_CHIPS)

    DECK_HEIGHT = CELL_SIZE

    DECK_MAX_X = DECK_MIN_X + DECK_WIDTH

    DECK_STEP = CELL_SIZE + DECK_DISTANCE_BETWEEN_CHIPS

    CELL_BORDER_SIZE = 1

    BACKGROUND_FILL_CHIP_BORDER_SIZE = HALF_OF_CELL_SIZE

    CURRENT_CHIP_BORDER_SIZE = 3

    N_BUTTONS = 3

    BUTTONS_MIN_X = DECK_MAX_X + CELL_SIZE

    BUTTONS_MIN_Y = DECK_MIN_Y

    BUTTON_WIDTH = CELL_SIZE * 2.2

    DISTANCE_BETWEEN_BUTTONS = DECK_DISTANCE_BETWEEN_CHIPS

    BUTTONS_WIDTH = \
        (N_BUTTONS * BUTTON_WIDTH + (N_BUTTONS - 1) * DISTANCE_BETWEEN_BUTTONS)

    BUTTONS_MAX_X = BUTTONS_MIN_X + BUTTONS_WIDTH

    BUTTONS_STEP = BUTTON_WIDTH + DISTANCE_BETWEEN_BUTTONS

    WIDTH = (DISPLAYED_PART_OF_FIELD_WIDTH +
             2 * HALF_OF_CELL_SIZE)

    HEIGHT = (HALF_OF_CELL_SIZE +
              DISPLAYED_PART_OF_FIELD_HEIGHT +
              LOWER_PANEL_HEIGHT)


# перечисление "константы игры".
class GameConstants:
    WHITE_COLOR = pygame.Color("white")

    BLACK_COLOR = pygame.Color("black")

    GRAY_COLOR = pygame.Color("#A9A9A9")

    GREEN_COLOR = pygame.Color("green")

    RED_COLOR = pygame.Color("red")

    PURPLE_COLOR = pygame.Color("purple")

    BLUE_COLOR = pygame.Color("#1E90FF")

    SHIFT_OF_DISPLAYED_PART_OF_FIELD_KEYS = (
        pygame.K_w,
        pygame.K_s,
        pygame.K_a,
        pygame.K_d,
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_c)

    CHOICE_OF_DECK_CHIP_KEYS = (
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6)

    SIMPLE_ACTIONS_KEYS = (
        pygame.K_b,
        pygame.K_m,
        pygame.K_e,
        pygame.K_f,
        pygame.K_r,
        pygame.K_g,
        pygame.K_x)

    CURRENT_CHIP_INDEX_MIN_VALUE = -1


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WindowParameters.WIDTH,
                                      WindowParameters.HEIGHT))

    pygame.display.set_caption("Квиркл")

    field = Field()

    field_copy = field.copy()

    heap = Heap()

    decks = [Deck(heap.give_chips(Deck.N_CHIPS_MAX_VALUE))]


    def draw_field(field_for_draw: Field) -> None:
        """
        рисует игровое поле.
        :param field_for_draw: отрисовываемое
        игровое поле.
        """

        validate_object_type(field, Field)

        min_x = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X
        max_x = min_x + WindowParameters.DISPLAYED_PART_OF_FIELD_WIDTH

        min_y = WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y
        max_y = max_x

        for x in range(min_x, max_x, WindowParameters.CELL_SIZE):
            for y in range(min_y, max_y, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(
                    x,
                    y,
                    WindowParameters.CELL_SIZE,
                    WindowParameters.CELL_SIZE)

                cell_column_index = ((x - min_x) //
                                     WindowParameters.CELL_SIZE +
                                     field_for_draw.cell_column_index_shift)

                cell_row_index = ((y - min_y) //
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
                        if field_for_draw.n_put_up_chips == 1:
                            chip_border_color = GameConstants.GRAY_COLOR
                        elif field_for_draw.is_last_choice_correct():
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


    def get_rects(
            left_corner_x: int,
            right_corner_x: int,
            y: int,
            step: int,
            rect_sizes: tuple[int, int]) -> list[pygame.Rect]:
        """
        возвращает однотипные прямоугольники
        :param left_corner_x: самая левая абсцисса, относящаяся
        к прямоугольникам;
        :param right_corner_x: самая правая абсцисса, относящаяся
        к прямоугольникам;
        :param y: самая верхняя ордината, относящаяся к прямоугольникам;
        :param step: шаг цикла (расстояние от левой стороны прямоугольника
        до левой стороны его соседа);
        :param rect_sizes: размеры прямоугольника.
        :return: однотипные прямоугольники.
        """

        rects = []

        for x in range(left_corner_x, right_corner_x, step):
            rect = pygame.Rect(x, y, rect_sizes[0], rect_sizes[1])

            rects.append(rect)

        return rects


    def draw_deck(
            rects: list[pygame.Rect],
            deck_for_draw: Deck,
            current_chip_index: int,
            indexes_of_exchanged_chips: list[int],
            indexes_of_new_chips: list[int]) -> None:
        """
        отрисовывает колоду фишек.
        :param rects: прямоугольники, в которых располагаются
        фишки.
        :param deck_for_draw: отрисовываемая колода
        фишек;
        :param current_chip_index: индекс текущей фишки;
        :param indexes_of_exchanged_chips: индексы обменянных
        фишек.
        :param indexes_of_new_chips: индексы новых фишек.
        """

        validate_object_type(deck_for_draw, Deck)

        validate_int_value(
            current_chip_index,
            (GameConstants.CURRENT_CHIP_INDEX_MIN_VALUE,
             Deck.CHIP_INDEX_MAX_VALUE))

        validate_container_elements_type(indexes_of_exchanged_chips, int)
        validate_container_elements_type(indexes_of_new_chips, int)

        chip_index = 0

        for rect in rects:
            chip = deck_for_draw.chip(chip_index)

            if chip is not None:
                pygame.draw.rect(
                    screen,
                    GameConstants.BLACK_COLOR,
                    rect,
                    WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)

                chip.draw_figure(screen, (rect.x, rect.y), WindowParameters.CELL_SIZE)

                if chip_index == current_chip_index:
                    pygame.draw.rect(
                        screen,
                        GameConstants.PURPLE_COLOR,
                        rect,
                        WindowParameters.CURRENT_CHIP_BORDER_SIZE)

                is_index_of_exchanged_chip = chip_index in indexes_of_exchanged_chips
                is_index_of_new_chip = chip_index in indexes_of_new_chips

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


    def draw_buttons(
            rects_of_buttons: list[pygame.Rect],
            labels: list[str]) -> None:
        """

        :param rects_of_buttons:
        :return:
        """

        validate_container_elements_type(rects_of_buttons, pygame.Rect)

        i = 0
        for rect in rects_of_buttons:
            pygame.draw.rect(
                screen,
                GameConstants.BLACK_COLOR,
                rect,
                WindowParameters.BACKGROUND_FILL_CHIP_BORDER_SIZE)

            font = pygame.font.Font("resources/fonts/unbounded bold.ttf", 18)

            text_surface = font.render(
                labels[i],
                True,
                GameConstants.WHITE_COLOR,
                GameConstants.BLACK_COLOR)

            text_rect = text_surface.get_rect(center=rect.center)

            screen.blit(text_surface, text_rect)

            i += 1


    def is_mouse_on_the_field(mouse_pos: tuple[int, int]) -> bool:
        """
        возвращает значение 'истина', если мышь в момент клика
        была на игровом поле, в противном случае - 'ложь'.
        :param mouse_pos: позиция
        :return: 'истина' или 'ложь'.
        """

        validate_container_elements_type(mouse_pos, int)

        x, y = mouse_pos

        return \
            ((WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_X <= x <=
              WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_X) and
             (WindowParameters.DISPLAYED_PART_OF_FIELD_MIN_Y <= y <=
              WindowParameters.DISPLAYED_PART_OF_FIELD_MAX_Y))


    def get_cell_indexes_by_mouse_pos(
            mouse_pos: tuple[int, int],
            viewed_field: Field) -> tuple[int, int]:
        """
        возвращает индексы строки и столбца клетки
        игрового поля по позиции мыши в момент клика.
        :param mouse_pos: позиция мыши в окне на
        момент совершения клика;
        :param viewed_field: проcматриваемое игровое
        поле;
        :return: индексы строки и столбца клетки
        игрового поля по позиции мыши.
        """

        validate_container_elements_type(mouse_pos, int)

        validate_object_type(viewed_field, Field)

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
            choice_cell_indexes: tuple[int, int],
            field_for_edit: Field,
            chip_for_putting_up: Chip) -> None:
        """
        обрабатывает событие клика левой клавишью
        мыши по сетке игрового поля.
        :param choice_cell_indexes: индексы строки
        и столбца клетки изменяемого игрового поля,
        которую пользователь выбрал для выставления
        фишки на поле;
        :param field_for_edit: изменяемое игровое
        поле;
        :param chip_for_putting_up: фишка для
        выставления на поле.
        """

        validate_container_elements_type(choice_cell_indexes, int)

        validate_object_type(field_for_edit, Field)
        validate_object_type(chip_for_putting_up, Chip)

        if not field_for_edit.has_chip_in_this_cell(choice_cell_indexes):
            field_for_edit.place_chip(chip_for_putting_up, choice_cell_indexes)

        if not field_for_edit.has_last_choice_init_value() and \
                choice_cell_indexes != field_for_edit.last_choice:
            field_for_edit.remove_chip(field_for_edit.last_choice)

        field_for_edit.last_choice = choice_cell_indexes


    def return_chip_back_to_the_deck(
            current_chip_parameters: tuple[Chip, int],
            deck: Deck) -> None:
        """
        возвращает фишку, выставленную на игровое поле,
        обратно в колоду.
        :param current_chip_parameters: параметры текущей
        фишки (объект класса Chip и индекс места в колоде);
        :param deck: колода фишек.
        """

        validate_object_type(deck, Deck)

        deck.place_chip(*current_chip_parameters)

        if not field.has_last_choice_init_value():
            field.remove_chip(field.last_choice)

            field.reset_last_choice()


    def make_exchange_of_chip(
            chips_deck: Deck,
            current_chip_parameters: tuple[Chip, int],
            indexes_of_exchanged_chips: list[int]) -> None:
        """
        производит обмен текущей фишки колоды, если это возможно.
        :param game_field: игровое поле;
        :param chips_heap: "куча" фишек;
        :param chips_deck: колода фишек;
        :param current_chip_parameters: параметры текущей
        фишки (объект класса Chip и индекс места в колоде);
        :param indexes_of_exchanged_chips: индексы обменянных
        фишек в колоде.
        """

        validate_object_type(chips_deck, Deck)

        validate_container_elements_type(indexes_of_exchanged_chips, int)

        if (not heap.is_empty() and
                len(indexes_of_exchanged_chips) < heap.n_chips() and
                current_chip_parameters[1] not in indexes_of_exchanged_chips and
                current_chip_parameters[0] is not None and
                field.has_last_choice_init_value()):
            substitute = \
                heap.make_an_exchange_of_chips([current_chip_parameters[0]])

            return_chip_back_to_the_deck(
                (substitute, current_chip_parameters[1]),
                chips_deck)

            indexes_of_exchanged_chips.append(current_chip_parameters[1])


    def make_exchange_of_all_unexchanged_chips(
            chips_deck: Deck,
            indexes_of_exchanged_chips: list[int]) -> tuple[Chip, int, list[int]]:
        """
        производит обмен все необменянных колоды.
        :param chips_deck: колода фишек.
        :return: текущая фишка, индекс места текущей фишки в
        колоде, список индексов мест обменянных фишек колоды.
        :param indexes_of_exchanged_chips: индексы обменянных
        фишек в колоде.
        """

        validate_object_type(chips_deck, Deck)

        validate_container_elements_type(indexes_of_exchanged_chips, int)

        indexes_of_chips_to_exchange = \
            list(set(chips_deck.get_non_empty_places_for_chips_indexes()) -
                 set(indexes_of_exchanged_chips))

        deck_returned_content = \
            copy(chips_deck.content_on_places(indexes_of_chips_to_exchange))

        new_deck_content = heap.make_an_exchange_of_chips(deck_returned_content)

        if new_deck_content is not None:
            n_unexchanged_chips = \
                (len(indexes_of_chips_to_exchange) - len(new_deck_content))

            if n_unexchanged_chips:
                indexes_of_chips_to_exchange = \
                    indexes_of_chips_to_exchange[:-n_unexchanged_chips]

            indexes_of_exchanged_chips = \
                list(set(indexes_of_exchanged_chips) | set(indexes_of_chips_to_exchange))

            chips_deck.place_on_places(
                new_deck_content,
                indexes_of_chips_to_exchange)

        return None, -1, indexes_of_exchanged_chips


    def complete_the_move(
            chips_deck: Deck) -> tuple[Chip, int, list[int], list[int]]:
        """
        завершает ход игрока.
        :param chips_deck: колода фишек;
        :return текущая фишка, индекс места текущей фишки в колоде, список
        индексов мест обменянных фишек колоды, список индексов мест новых
        фишек колоды.
        """

        validate_object_type(chips_deck, Deck)

        indexes_of_new_chips = chips_deck.get_empty_places_for_chips_indexes()

        extra_chips = chips_deck.replenish(heap.give_chips(Deck.N_CHIPS_MAX_VALUE))

        if extra_chips:
            heap.return_chips(extra_chips)
        elif not chips_deck.is_full():
            indexes_of_new_chips = \
                list(set(indexes_of_new_chips) -
                     set(chips_deck.get_empty_places_for_chips_indexes()))

        return None, -1, [], indexes_of_new_chips


    def get_current_chip_index(
            certain_value: object,
            container: list | tuple) -> int:
        """
        возвращает индекс текущей фишки исходя из позиции,
        которую занимает элемент с определенным значением
        в контейнере.
        :param certain_value: определенное значение;
        :param container: контейнер;
        :return: индекс текущей фишки.
        """

        return container.index(certain_value)


    def get_new_current_chip_parameters(
            certain_value: object,
            container: list | tuple,
            game_field: Field,
            chips_deck: Deck,
            current_chip_parameters: tuple[Chip, int]) -> tuple[Chip | None, int | None]:
        """
        возвращает новые параметры текущей фишки.
        :param certain_value: определенное значение;
        :param container: контейнер;
        :param game_field: игровое поле;
        :param chips_deck: колода фишек;
        :param current_chip_parameters: параметры текущей
        фишки (объект класса Chip и индекс места в колоде);
        :return: новые параметры текущей фишки (объект класса
        Chip и индекс места в колоде).
        """

        validate_object_type(game_field, Field)
        validate_object_type(chips_deck, Deck)

        chip_index = container.index(certain_value)

        chip = chips_deck.chip(chip_index)

        if chip is not None:
            if (current_chip_parameters[0] is not None and
                    chip_index != current_chip_parameters[1]):
                return_chip_back_to_the_deck(
                    current_chip_parameters,
                    chips_deck)

            return chip, chip_index
        else:
            return None, None


    def game_cycle(player_deck: Deck) -> None:
        """
        функция игрового цикла.
        """

        global field

        global field_copy

        chip_was_put_up_sound = pygame.mixer.Sound(
            "resources/sounds/chip_was_put_up.wav")

        shift_of_displayed_part_of_field_sound = pygame.mixer.Sound(
            "resources/sounds/shift_of_displayed_part_of_field.wav")

        is_shift_of_displayed_part_blocked = False

        are_sounds_muted = False

        current_chip = None
        current_chip_index = -1

        exchanged_chips_indexes = []
        new_chips_indexes = []

        deck_chips_rects = get_rects(
            WindowParameters.DECK_MIN_X,
            WindowParameters.DECK_MAX_X,
            WindowParameters.DECK_MIN_Y,
            WindowParameters.DECK_STEP,
            (WindowParameters.CELL_SIZE,
             WindowParameters.CELL_SIZE))

        buttons_rects = get_rects(
            WindowParameters.BUTTONS_MIN_X,
            WindowParameters.BUTTONS_MAX_X,
            WindowParameters.BUTTONS_MIN_Y,
            WindowParameters.BUTTONS_STEP,
            (WindowParameters.BUTTON_WIDTH,
             WindowParameters.CELL_SIZE))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    deck_chips_mouse_choice_checks = \
                        [rect.collidepoint(pygame.mouse.get_pos())
                         for rect in deck_chips_rects]

                    if is_mouse_on_the_field(pygame.mouse.get_pos()):
                        cell_indexes = get_cell_indexes_by_mouse_pos(
                            pygame.mouse.get_pos(),
                            field)

                        cell_content = field.get_content_of_cell(cell_indexes)

                        if (event.button == 1 and
                                not isinstance(cell_content, Chip) and
                                current_chip is not None):
                            player_deck.remove_chip(current_chip_index)

                            if new_chips_indexes:
                                new_chips_indexes = []

                            field_copy = field.copy(copy_last_choice=True)

                            handle_left_click(cell_indexes, field_copy, current_chip)

                            field = field_copy.copy(copy_last_choice=True)
                        elif (event.button == 3 and
                              field.is_last_choice_correct() and
                              cell_indexes == field.last_choice):
                            field.reset_last_choice()

                            if not are_sounds_muted:
                                chip_was_put_up_sound.play()

                            current_chip = None
                            current_chip_index = -1
                    elif (True in deck_chips_mouse_choice_checks
                          and event.button == 1):
                        new_current_chip, new_current_chip_index = \
                            get_new_current_chip_parameters(
                                True,
                                deck_chips_mouse_choice_checks,
                                field,
                                player_deck,
                                (current_chip, current_chip_index))

                        if (new_current_chip is not None
                                and new_current_chip_index is not None):
                            current_chip, current_chip_index = new_current_chip, new_current_chip_index
                    elif buttons_rects[0].collidepoint(pygame.mouse.get_pos()):
                        make_exchange_of_chip(
                            player_deck,
                            (current_chip, current_chip_index),
                            exchanged_chips_indexes)
                    elif buttons_rects[1].collidepoint(pygame.mouse.get_pos()):
                        if (not player_deck.is_empty() and
                                field.has_last_choice_init_value()):
                            (current_chip,
                             current_chip_index,
                             exchanged_chips_indexes) = \
                                make_exchange_of_all_unexchanged_chips(
                                    player_deck,
                                    exchanged_chips_indexes)
                    elif buttons_rects[2].collidepoint(pygame.mouse.get_pos()):
                        if field.has_last_choice_init_value():
                            (current_chip,
                             current_chip_index,
                             exchanged_chips_indexes,
                             new_chips_indexes) = \
                                complete_the_move(player_deck)
                elif event.type == pygame.KEYDOWN:
                    if event.key in GameConstants.SIMPLE_ACTIONS_KEYS:
                        match event.key:
                            case pygame.K_b:
                                is_shift_of_displayed_part_blocked = \
                                    not is_shift_of_displayed_part_blocked
                            case pygame.K_m:
                                are_sounds_muted = not are_sounds_muted
                            case pygame.K_e:
                                make_exchange_of_chip(
                                    player_deck,
                                    (current_chip, current_chip_index),
                                    exchanged_chips_indexes)
                            case pygame.K_f:
                                if field.has_last_choice_init_value():
                                    (current_chip,
                                     current_chip_index,
                                     exchanged_chips_indexes,
                                     new_chips_indexes) = \
                                        complete_the_move(player_deck)
                            case pygame.K_r:
                                if (not player_deck.is_empty() and
                                        field.has_last_choice_init_value()):
                                    (current_chip,
                                     current_chip_index,
                                     exchanged_chips_indexes) = \
                                        make_exchange_of_all_unexchanged_chips(
                                            player_deck,
                                            exchanged_chips_indexes)
                            case pygame.K_g:
                                if not field.has_last_choice_init_value():
                                    return_chip_back_to_the_deck(
                                        (current_chip, current_chip_index),
                                        player_deck)
                    elif event.key in GameConstants.CHOICE_OF_DECK_CHIP_KEYS:
                        new_current_chip, new_current_chip_index = \
                            get_new_current_chip_parameters(
                                event.key,
                                GameConstants.CHOICE_OF_DECK_CHIP_KEYS,
                                field,
                                player_deck,
                                (current_chip, current_chip_index))

                        if (new_current_chip is not None
                                and new_current_chip_index is not None):
                            current_chip, current_chip_index = new_current_chip, new_current_chip_index
                    elif (is_shift_of_displayed_part_blocked is False and
                          event.key in GameConstants.SHIFT_OF_DISPLAYED_PART_OF_FIELD_KEYS):
                        match event.key:
                            case pygame.K_w | pygame.K_UP:
                                field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_UP)
                            case pygame.K_s | pygame.K_DOWN:
                                field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_DOWN)
                            case pygame.K_a | pygame.K_LEFT:
                                field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_LEFT)
                            case pygame.K_d | pygame.K_RIGHT:
                                field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_RIGHT)
                            case pygame.K_c:
                                field.reset_cell_row_index_shift()
                                field.reset_cell_column_index_shift()

                        if not are_sounds_muted:
                            shift_of_displayed_part_of_field_sound.play()

            screen.fill(pygame.Color("white"))

            draw_field(field)

            draw_deck(deck_chips_rects,
                      player_deck,
                      current_chip_index,
                      exchanged_chips_indexes,
                      new_chips_indexes)

            draw_buttons(buttons_rects, ["Обмен", "Обмен *", "Ход"])

            pygame.display.flip()


    game_cycle(decks[0])
