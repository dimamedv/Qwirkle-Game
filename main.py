from field import Field
from chip import Chip

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

                cell_content = field_for_draw.get_content_of_cell(
                    (cell_row_index, cell_column_index))

                if isinstance(cell_content, Chip):
                    pygame.draw.rect(screen,
                                     pygame.Color("black"),
                                     rect,
                                     WindowParameters.CELL_SIZE // 2)

                    cell_content.draw_figure(screen, (x, y), WindowParameters.CELL_SIZE)

                    if (cell_row_index, cell_column_index) == field_for_draw.last_choice:
                        if field_for_draw.has_at_least_one_neighboring_chip_to_this_chip(
                                (cell_row_index, cell_column_index)):
                            border_color = pygame.Color("Green")
                        else:
                            border_color = pygame.Color("Red")

                        pygame.draw.rect(screen, border_color, rect, 2)
                else:
                    pygame.draw.rect(screen, pygame.Color("black"), rect, 1)


    def handle_click(
            mouse_pos: tuple[int, int],
            field_for_edit: Field) -> None:
        """
        обрабатывает событие клика мыши по сетке
        игрового поля.
        :param mouse_pos: позиция мыши в окне на
        момент совершения клика;
        :param field_for_edit: изменяемое игровое
        поле.
        """

        x, y = mouse_pos

        cell_column_index = (x // WindowParameters.CELL_SIZE +
                             field_for_edit.cell_column_index_shift)

        cell_row_index = (y // WindowParameters.CELL_SIZE +
                          field_for_edit.cell_row_index_shift)

        # помещение фишки в клетку:
        if not field_for_edit.has_chip_in_this_cell((cell_row_index,
                                                     cell_column_index)):
            field_for_edit.place_chip(Chip(Chip.Figures.EIGHT_PT_STAR,
                                           pygame.Color("orange")),
                                      (cell_row_index,
                                       cell_column_index))

        if field_for_edit.last_choice != (-1, -1) and \
                (cell_row_index, cell_column_index) != field_for_edit.last_choice:
            field_for_edit.remove_chip(field_for_edit.last_choice)

        field_for_edit.last_choice = (cell_row_index,
                                      cell_column_index)


    def game_cycle() -> None:
        """
        функция игрового цикла.
        """

        # глобальная переменная игровго поля.
        global field

        # глобальная переменная копии игровго поля.
        global field_copy

        # основной игровой цикл:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        field_copy = field.copy(copy_last_choice=True)

                        handle_click(pygame.mouse.get_pos(), field_copy)

                        field = field_copy.copy(copy_last_choice=True)
                    elif event.button == 3 and field.is_correct_last_choice():
                        field.reset_last_choice()

            screen.fill(pygame.Color("white"))

            # рисование поля:
            draw_field(field)

            # обновление экрана:
            pygame.display.flip()


    game_cycle()
