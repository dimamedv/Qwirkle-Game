from field import Field
from chip import Chip
from heap import Heap

import sys
import enum

import pygame


# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    # размер клетки;
    CELL_SIZE = 50

    # ширина окна игры;
    WIDTH = CELL_SIZE * Field.DISPLAYED_PART_N_CELLS_IN_WIDTH

    # высота окна игры.
    HEIGHT = CELL_SIZE * Field.DISPLAYED_PART_N_CELLS_IN_HEIGHT


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
        pygame.K_RIGHT)


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

        for x in range(0, WindowParameters.WIDTH, WindowParameters.CELL_SIZE):
            for y in range(0, WindowParameters.HEIGHT, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

                cell_column_index = (x // WindowParameters.CELL_SIZE +
                                     field_for_draw.cell_column_index_shift)

                cell_row_index = (y // WindowParameters.CELL_SIZE +
                                  field_for_draw.cell_row_index_shift)

                cell_indexes = (cell_row_index, cell_column_index)

                cell_content = field_for_draw.get_content_of_cell(cell_indexes)

                if isinstance(cell_content, Chip):
                    pygame.draw.rect(screen,
                                     GameConstants.BLACK_COLOR,
                                     rect,
                                     WindowParameters.CELL_SIZE // 2)

                    cell_content.draw_figure(screen, (x, y), WindowParameters.CELL_SIZE)

                    if cell_indexes == field_for_draw.last_choice:
                        if field_for_draw.n_put_up_chips == 1:
                            chip_border_color = GameConstants.BLUE_COLOR_FOR_CHIP_BORDER
                        elif field_for_draw.has_at_least_one_neighboring_chip_to_this_chip(
                                cell_indexes):
                            chip_border_color = GameConstants.GREEN_COLOR_FOR_CHIP_BORDER
                        else:
                            chip_border_color = GameConstants.RED_COLOR_FOR_CHIP_BORDER

                        pygame.draw.rect(screen, chip_border_color, rect, 2)
                else:
                    pygame.draw.rect(screen, GameConstants.BLACK_COLOR, rect, 1)


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

        cell_column_index = (x // WindowParameters.CELL_SIZE +
                             viewed_field.cell_column_index_shift)

        cell_row_index = (y // WindowParameters.CELL_SIZE +
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

        current_chip = None

        # основной игровой цикл:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cell_indexes = get_cell_indexes_by_mouse_pos(
                        pygame.mouse.get_pos(),
                        field)

                    cell_content = field.get_content_of_cell(cell_indexes)

                    if event.button == 1 and not isinstance(cell_content, Chip):
                        field_copy = field.copy(copy_last_choice=True)

                        if current_chip is None:
                            current_chip = heap.give_chip()

                        handle_left_click(cell_indexes, field_copy, current_chip)

                        field = field_copy.copy(copy_last_choice=True)
                    elif (event.button == 3 and
                          field.is_correct_last_choice() and
                          cell_indexes == field.last_choice):
                        field.reset_last_choice()

                        if not are_sounds_muted:
                            chip_was_put_up_sound.play()

                        current_chip = None
                elif event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_b:
                            is_shift_of_displayed_part_blocked = \
                                not is_shift_of_displayed_part_blocked
                        case pygame.K_m:
                            are_sounds_muted = not are_sounds_muted

                    if is_shift_of_displayed_part_blocked is False:
                        if event.key == pygame.K_c:
                            field.reset_cell_row_index_shift()
                            field.reset_cell_column_index_shift()
                        elif event.key in GameConstants.SHIFT_OF_DISPLAYED_PART_OF_FIELD_KEYS:
                            match event.key:
                                case pygame.K_w | pygame.K_UP:
                                    field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_UP)
                                case pygame.K_s | pygame.K_DOWN:
                                    field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_DOWN)
                                case pygame.K_a | pygame.K_LEFT:
                                    field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_LEFT)
                                case pygame.K_d | pygame.K_RIGHT:
                                    field.shift_displayed_part(Field.SHIFT_DISPLAYED_PART_RIGHT)

                            if not are_sounds_muted:
                                shift_of_displayed_part_of_field_sound.play()

            screen.fill(pygame.Color("white"))

            # отрисовка поля:
            draw_field(field)

            # обновление экрана:
            pygame.display.flip()


    game_cycle()
