from field import Field
from chip import Chip
from heap import Heap
from deck import Deck

import sys
import enum

import pygame


# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    # размер клетки.
    CELL_SIZE = 50

    # половина размера клетки.
    HALF_OF_CELL_SIZE = CELL_SIZE // 2

    # ширина отображаемой части игрового поля.
    DISPLAYED_PART_OF_FIELD_WIDTH = \
        (CELL_SIZE *
         Field.DISPLAYED_PART_N_CELLS_IN_WIDTH)

    # высота отображаемой части игрового поля.
    DISPLAYED_PART_OF_FIELD_HEIGHT = \
        (CELL_SIZE *
         Field.DISPLAYED_PART_N_CELLS_IN_HEIGHT)

    # минимальная абсцисса, относящаяся к отображаемой
    # части игрового поля.
    DISPLAYED_PART_OF_FIELD_MIN_X = \
        HALF_OF_CELL_SIZE

    # минимальная ордината, относящаяся к отображаемой
    # части игрового поля.
    DISPLAYED_PART_OF_FIELD_MIN_Y = \
        DISPLAYED_PART_OF_FIELD_MIN_X

    # максимальная абсцисса, относящаяся к отображаемой
    # части игрового поля.
    DISPLAYED_PART_OF_FIELD_MAX_X = \
        (DISPLAYED_PART_OF_FIELD_MIN_X +
         DISPLAYED_PART_OF_FIELD_WIDTH)

    # максимальная ордината, относящаяся к отображаемой
    # части игрового поля.
    DISPLAYED_PART_OF_FIELD_MAX_Y = \
        (DISPLAYED_PART_OF_FIELD_MIN_Y +
         DISPLAYED_PART_OF_FIELD_HEIGHT)

    # высота нижней панели.
    LOWER_PANEL_HEIGHT = 150

    # ширина окна игры.
    WIDTH = (DISPLAYED_PART_OF_FIELD_WIDTH +
             2 * HALF_OF_CELL_SIZE)

    # высота окна игры.
    HEIGHT = (HALF_OF_CELL_SIZE +
              DISPLAYED_PART_OF_FIELD_HEIGHT +
              LOWER_PANEL_HEIGHT)

    # абсцисса левого верхнего угла колоды.
    DECK_LEFT_CORNER_X = HALF_OF_CELL_SIZE

    # абсцисса правого верхнего угла колоды.
    DECK_RIGHT_CORNER_Y = \
        (DISPLAYED_PART_OF_FIELD_HEIGHT +
         2 * HALF_OF_CELL_SIZE)

    # расстояние между фишками в колоде.
    DECK_DISTANCE_BETWEEN_CHIPS = 10

    # ширина колоды.
    DECK_WIDTH = \
        (Deck.N_CHIPS_MAX_VALUE * CELL_SIZE +
         (Deck.N_CHIPS_MAX_VALUE - 1) * DECK_DISTANCE_BETWEEN_CHIPS)

    # высота колоды.
    DECK_HEIGHT = CELL_SIZE


# перечисление "константы игры".
class GameConstants:
    # черный цвет.
    BLACK_COLOR = pygame.Color("black")

    # синий цвет для каемки первой выложенной
    # на игровое поле фишки.
    BLUE_COLOR_FOR_CHIP_BORDER = pygame.Color("#1E90FF")

    # зеленый цвет для каемки фишки, которую пользователь
    # хочет выложить на поле и которая прошла валидацию.
    GREEN_COLOR_FOR_CHIP_BORDER = pygame.Color("green")

    # красный цвет для каемки фишки, которую пользователь
    # хочет выложить на поле и которая прошла валидацию.
    RED_COLOR_FOR_CHIP_BORDER = pygame.Color("red")

    PURPLE_COLOR_FOR_CHOSEN_DECK_CHIP = pygame.Color("purple")

    # клавиши для сдвига отображаемой части
    # игрового поля.
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

    # клавиши выбора фишки колоды.
    CHOICE_OF_DECK_CHIP_KEYS = (
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6)

    # клавиши простых действий
    SIMPLE_ACTIONS_KEYS = (
        pygame.K_b,
        pygame.K_m,
        pygame.K_e)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WindowParameters.WIDTH,
                                      WindowParameters.HEIGHT))

    # заголовок окна.
    pygame.display.set_caption("Квиркл")

    # игровое поле.
    field = Field()

    # копия игрового поля.
    field_copy = field.copy()


    def draw_field(field_for_draw: Field) -> None:
        """
        рисует игровое поле.
        :param field_for_draw: отрисовываемое
        игровое поле.
        """

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
                        WindowParameters.CELL_SIZE // 2)

                    cell_content.draw_figure(
                        screen,
                        (x, y),
                        WindowParameters.CELL_SIZE)

                    if cell_indexes == field_for_draw.last_choice:
                        if field_for_draw.n_put_up_chips == 1:
                            chip_border_color = \
                                GameConstants.BLUE_COLOR_FOR_CHIP_BORDER
                        elif field_for_draw.is_last_choice_correct():
                            chip_border_color = \
                                GameConstants.GREEN_COLOR_FOR_CHIP_BORDER
                        else:
                            chip_border_color = \
                                GameConstants.RED_COLOR_FOR_CHIP_BORDER

                        pygame.draw.rect(
                            screen,
                            chip_border_color,
                            rect,
                            2)
                else:
                    pygame.draw.rect(
                        screen,
                        GameConstants.BLACK_COLOR,
                        rect,
                        1)


    def draw_deck(
            deck_for_draw: Deck,
            current_chip_index: int) -> None:
        """
        отрисовывает колоду фишек.
        :param deck_for_draw: отрисовываемая колода
        фишек;
        :param current_chip_index: индекс текущей фишки.
        """

        y = WindowParameters.DECK_RIGHT_CORNER_Y

        left_corner_x = WindowParameters.DECK_LEFT_CORNER_X
        right_corner_x = left_corner_x + WindowParameters.DECK_WIDTH

        step = WindowParameters.CELL_SIZE + WindowParameters.DECK_DISTANCE_BETWEEN_CHIPS

        chip_index = 0

        for x in range(left_corner_x, right_corner_x, step):
            rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

            chip = deck_for_draw.chip(chip_index)

            if chip is not None:
                pygame.draw.rect(
                    screen,
                    GameConstants.BLACK_COLOR,
                    rect,
                    WindowParameters.CELL_SIZE // 2)

                chip.draw_figure(screen, (x, y), WindowParameters.CELL_SIZE)

                if chip_index == current_chip_index:
                    pygame.draw.rect(
                        screen,
                        GameConstants.PURPLE_COLOR_FOR_CHOSEN_DECK_CHIP,
                        rect,
                        2)
            else:
                pygame.draw.rect(
                    screen,
                    GameConstants.BLACK_COLOR,
                    rect,
                    1)

            chip_index += 1


    def is_mouse_on_the_field(mouse_pos: tuple[int, int]) -> bool:
        """
        возвращает значение 'истина', если мышь в момент клика
        была на игровом поле, в противном случае - 'ложь'.
        :param mouse_pos: позиция
        :return: 'истина' или 'ложь'.
        """

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

        # помещение фишки в клетку:
        if not field_for_edit.has_chip_in_this_cell(choice_cell_indexes):
            field_for_edit.place_chip(chip_for_putting_up, choice_cell_indexes)

        if not field_for_edit.has_last_choice_init_value() and \
                choice_cell_indexes != field_for_edit.last_choice:
            field_for_edit.remove_chip(field_for_edit.last_choice)

        field_for_edit.last_choice = choice_cell_indexes


    def return_chip_back_to_the_deck(
            chip: Chip,
            chip_index: int,
            field: Field,
            deck: Deck) -> None:
        """
        возвращает фишку, выставленную на игровое поле,
        обратно в колоду.
        :param chip: фишка, выставленная на игровое поле;
        :param chip_index: индекс фишки в колоде;
        :param field: игровое поле;
        :param deck: колода фишек.
        """

        deck.place_chip(chip, chip_index)

        if not field.has_last_choice_init_value():
            field.remove_chip(field.last_choice)

            field.reset_last_choice()


    def game_cycle() -> None:
        """
        функция игрового цикла.
        """

        # глобальная переменная игровго поля.
        global field

        # глобальная переменная копии игровго поля.
        global field_copy

        # звук выложенной на поле фишки.
        chip_was_put_up_sound = pygame.mixer.Sound(
            "resources/sounds/chip_was_put_up.wav")

        # звук сдвига отображаемой части игрового поля.
        shift_of_displayed_part_of_field_sound = pygame.mixer.Sound(
            "resources/sounds/shift_of_displayed_part_of_field.wav")

        # флаг, сообщающий о том, заблокирован сдвиг
        # отображаемой части игрового поля или нет.
        is_shift_of_displayed_part_blocked = False

        # флаг, сообщающий о том, выключены звуки
        # или нет.
        are_sounds_muted = False

        heap = Heap()

        deck = Deck(heap.give_chips(Deck.N_CHIPS_MAX_VALUE))

        current_chip = None
        current_chip_index = -1

        exchanged_chips_indexes = []

        # основной игровой цикл:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN and
                      is_mouse_on_the_field(pygame.mouse.get_pos())):
                    cell_indexes = get_cell_indexes_by_mouse_pos(
                        pygame.mouse.get_pos(),
                        field)

                    cell_content = field.get_content_of_cell(cell_indexes)

                    if (event.button == 1 and
                            not isinstance(cell_content, Chip) and
                            current_chip is not None):
                        field_copy = field.copy(copy_last_choice=True)

                        deck.remove_chip(current_chip_index)

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
                elif event.type == pygame.KEYDOWN:
                    if event.key in GameConstants.SIMPLE_ACTIONS_KEYS:
                        match event.key:
                            case pygame.K_b:
                                is_shift_of_displayed_part_blocked = \
                                    not is_shift_of_displayed_part_blocked
                            case pygame.K_m:
                                are_sounds_muted = not are_sounds_muted
                            case pygame.K_e:
                                if (current_chip_index not in exchanged_chips_indexes and
                                        current_chip is not None):
                                    exchanged_chips_indexes.append(current_chip_index)

                                    current_chip = heap.make_an_exchange_of_chips([current_chip])[0]

                                    return_chip_back_to_the_deck(
                                        current_chip,
                                        current_chip_index,
                                        field,
                                        deck)
                    elif event.key in GameConstants.CHOICE_OF_DECK_CHIP_KEYS:
                        chip_index = GameConstants.CHOICE_OF_DECK_CHIP_KEYS.index(event.key)

                        chip = deck.chip(chip_index)

                        if chip is not None:
                            if (current_chip is not None and
                                    chip_index != current_chip_index):
                                return_chip_back_to_the_deck(
                                    current_chip,
                                    current_chip_index,
                                    field,
                                    deck)

                            current_chip = chip
                            current_chip_index = chip_index
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

            # отрисовка поля:
            draw_field(field)

            # отрисовка колоды фишек:
            draw_deck(deck, current_chip_index)

            # обновление экрана:
            pygame.display.flip()


    game_cycle()
