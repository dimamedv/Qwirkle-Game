import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна игры
cell_size = 40
grid_width = 15
grid_height = 15
width = cell_size * grid_width
height = cell_size * grid_height
screen = pygame.display.set_mode((width, height))

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)

# Заголовок окна
pygame.display.set_caption("Qwirkle Game")


def draw_grid():
    for x in range(0, width, cell_size):  # Для каждой колонки
        for y in range(0, height, cell_size):  # Для каждой строки
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)  # Заливка экрана черным цветом
    draw_grid()  # Рисование сетки
    pygame.display.flip()  # Обновление экрана

