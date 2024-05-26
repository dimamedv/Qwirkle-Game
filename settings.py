import enum

import pygame

from field import Field
from deck import Deck

# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    # размер клетки.
    CELL_SIZE = 30

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
    LOWER_PANEL_HEIGHT = CELL_SIZE * 2

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

    # толщина границы клетки.
    CELL_BORDER_SIZE = 1

    # толщина контура прямоугольника
    # для заливки фишки чёрным цветом.
    BACKGROUND_FILL_CHIP_BORDER_SIZE = HALF_OF_CELL_SIZE

    # толщина каёмки текущей фишки.
    CURRENT_CHIP_BORDER_SIZE = 3


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
