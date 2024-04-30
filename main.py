import chip

import sys
import enum

import pygame


# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    # размер клетки;
    CELL_SIZE = 50

    # ширина сетки игрового поля;
    GRID_WIDTH = 14

    # высота сетки игрового поля;
    GRID_HEIGHT = 14

    # ширина окна игры;
    WIDTH = CELL_SIZE * GRID_WIDTH

    # высота окна игры.
    HEIGHT = CELL_SIZE * GRID_HEIGHT


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WindowParameters.WIDTH,
                                      WindowParameters.HEIGHT))

    # заголовок окна
    pygame.display.set_caption("Qwirkle Game")

    # сетка для хранения фишек
    grid = [[None for _ in range(WindowParameters.GRID_WIDTH)]
            for _ in range(WindowParameters.GRID_HEIGHT)]


    def draw_grid():
        for x in range(0, WindowParameters.WIDTH, WindowParameters.CELL_SIZE):
            for y in range(0, WindowParameters.HEIGHT, WindowParameters.CELL_SIZE):
                rect = pygame.Rect(x, y, WindowParameters.CELL_SIZE, WindowParameters.CELL_SIZE)

                grid_x = x // WindowParameters.CELL_SIZE
                grid_y = y // WindowParameters.CELL_SIZE

                if grid[grid_y][grid_x]:
                    pygame.draw.rect(screen,
                                     pygame.Color("black"),
                                     rect,
                                     WindowParameters.CELL_SIZE // 2)

                    chip.draw_figure(screen,
                                     x,
                                     y,
                                     WindowParameters.CELL_SIZE,
                                     pygame.Color("red"),
                                     chip.Figures.EIGHT_PT_STAR)
                else:
                    pygame.draw.rect(screen, pygame.Color("black"), rect, 1)


    def handle_click(pos, previous_chip_x, previous_chip_y):
        x, y = pos

        grid_x = x // WindowParameters.CELL_SIZE
        grid_y = y // WindowParameters.CELL_SIZE

        if previous_chip_x >= 0 and previous_chip_y >= 0:
            grid[previous_chip_y][previous_chip_x] = None

        # помещение фишки в клетку:
        if grid[grid_y][grid_x] is None:
            grid[grid_y][grid_x] = 'Red'

        return grid_x, grid_y


    def game_cycle():
        previous_chip_x, previous_chip_y = -1, -1

        # основной игровой цикл:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    previous_chip_x, previous_chip_y = handle_click(pygame.mouse.get_pos(),
                                                                    previous_chip_x,
                                                                    previous_chip_y)

            screen.fill(pygame.Color("white"))

            # рисование сетки:
            draw_grid()

            # обновление экрана:
            pygame.display.flip()


    game_cycle()
