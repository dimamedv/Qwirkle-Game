import enum

import pygame

from field import Field
from deck import Deck


# перечисление "константы окна игры".
class WindowParameters(enum.IntEnum):
    CELL_SIZE = 30

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

    LOWER_PANEL_HEIGHT = CELL_SIZE * 2

    WIDTH = (DISPLAYED_PART_OF_FIELD_WIDTH +
             2 * HALF_OF_CELL_SIZE)

    HEIGHT = (HALF_OF_CELL_SIZE +
              DISPLAYED_PART_OF_FIELD_HEIGHT +
              LOWER_PANEL_HEIGHT)

    DECK_MIN_X = HALF_OF_CELL_SIZE

    DECK_MIN_Y = \
        (DISPLAYED_PART_OF_FIELD_HEIGHT +
         2 * HALF_OF_CELL_SIZE)

    DECK_DISTANCE_BETWEEN_CHIPS = 10

    DECK_WIDTH = \
        (Deck.N_CHIPS_MAX_VALUE * CELL_SIZE +
         (Deck.N_CHIPS_MAX_VALUE - 1) * DECK_DISTANCE_BETWEEN_CHIPS)

    DECK_HEIGHT = CELL_SIZE

    CELL_BORDER_SIZE = 1

    BACKGROUND_FILL_CHIP_BORDER_SIZE = HALF_OF_CELL_SIZE

    CURRENT_CHIP_BORDER_SIZE = 3


# перечисление "константы игры".
class GameConstants:
    BLACK_COLOR = pygame.Color("black")

    BLUE_COLOR = pygame.Color("#1E90FF")

    GREEN_COLOR = pygame.Color("green")

    RED_COLOR = pygame.Color("red")

    PURPLE_COLOR = pygame.Color("purple")

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
        pygame.K_r,
        pygame.K_f,
        pygame.K_g)
