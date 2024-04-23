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

# Сетка для хранения фишек
grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

def draw_grid():
    for x in range(0, width, cell_size):  # Для каждой колонки
        for y in range(0, height, cell_size):  # Для каждой строки
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)
            if grid[y // cell_size][x // cell_size]:
                color = pygame.Color('red')  # Здесь можно использовать разные цвета
                pygame.draw.circle(screen, color, (x + cell_size // 2, y + cell_size // 2), cell_size // 3)

def handle_click(pos):
    x, y = pos
    grid_x = x // cell_size
    grid_y = y // cell_size
    if grid[grid_y][grid_x] is None:  # Если клетка пуста
        grid[grid_y][grid_x] = 'Red'  # Пример установки фишки, можно добавить выбор цвета


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    screen.fill(white)  # Заливка экрана черным цветом
    draw_grid()  # Рисование сетки
    pygame.display.flip()  # Обновление экрана