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
    WIDTH = CELL_SIZE * Field.Constants.GRID_WIDTH

    # высота окна игры.
    HEIGHT = CELL_SIZE * Field.Constants.GRID_HEIGHT


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WindowParameters.WIDTH,
                                      WindowParameters.HEIGHT))

    # заголовок окна
    pygame.display.set_caption("Квиркл")

    # игровое поле.
    field = Field()


    def draw_field():
        """
        рисует игровое поле.
        """

        for x in range(0, WindowParameters.WIDTH, WindowParameters.CELL_SIZE):
            for y in range(0, WindowParameters.HEIGHT, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

                cell_column_index = x // WindowParameters.CELL_SIZE
                cell_row_index = y // WindowParameters.CELL_SIZE

                cell_content = field.get_content_of_cell(cell_row_index,
                                                         cell_column_index)

                if isinstance(cell_content, Chip):
                    pygame.draw.rect(screen,
                                     pygame.Color("black"),
                                     rect,
                                     WindowParameters.CELL_SIZE // 2)

                    cell_content.draw_figure(screen, x, y, WindowParameters.CELL_SIZE)

                    if field.has_at_least_one_neighboring_chip_to_this_chip(cell_row_index,
                                                                            cell_column_index):
                        border_color = pygame.Color("Green")
                    else:
                        border_color = pygame.Color("Red")

                    pygame.draw.rect(screen, border_color, rect, 2)
                else:
                    pygame.draw.rect(screen, pygame.Color("black"), rect, 1)


    def handle_click(mouse_pos,
                     previous_chip_cell_row_index,
                     previous_chip_cell_column_index):
        """
        обрабатывает событие клика мыши по сетке игрового
        поля.
        :param mouse_pos: позиция мыши в окне на момент
        совершения клика;
        :param previous_chip_cell_row_index: индекс
        строки клетки игрового поля, в которую была помещена
        предыдущая фишка;
        :param previous_chip_cell_column_index: индекс
        столбца клетки игрового поля, в которую была помещена
        предыдущая фишка;
        """

        x, y = mouse_pos

        cell_column_index = x // WindowParameters.CELL_SIZE
        cell_row_index = y // WindowParameters.CELL_SIZE

        # помещение фишки в клетку:
        if not field.has_chip_in_this_cell(cell_row_index, cell_column_index):
            field.place_chip(Chip(Chip.Figures.DIAMOND, pygame.Color("purple")),
                             cell_row_index,
                             cell_column_index)

        if previous_chip_cell_row_index >= 0 and \
                previous_chip_cell_column_index >= 0 and \
                (previous_chip_cell_row_index != cell_row_index or
                 previous_chip_cell_column_index != cell_column_index):
            field.remove_chip(previous_chip_cell_row_index,
                              previous_chip_cell_column_index)

        return cell_row_index, cell_column_index


    def game_cycle():
        """
        функция игрового цикла.
        """

        previous_chip_cell_row_index, previous_chip_cell_column_index = -1, -1

        # основной игровой цикл:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        (previous_chip_cell_row_index,
                         previous_chip_cell_column_index) = handle_click(pygame.mouse.get_pos(),
                                                                         previous_chip_cell_row_index,
                                                                         previous_chip_cell_column_index)

            screen.fill(pygame.Color("white"))

            # рисование сетки:
            draw_field()

            # обновление экрана:
            pygame.display.flip()


    game_cycle()
