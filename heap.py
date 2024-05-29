from validators import *

from chip import Chip
from deck import Deck

import pygame

from random import shuffle, randint


# класс "куча (набор фишек)".
class Heap:
    GIVE_CHIPS_PARAMETER_MIN_VALUE = 1

    def __init__(self):
        """
        конструктор класса.
        """

        self.__content = []

        colors_of_figure = (
            pygame.Color(Chip.ColorsOfFigures.RED),
            pygame.Color(Chip.ColorsOfFigures.ORANGE),
            pygame.Color(Chip.ColorsOfFigures.YELLOW),
            pygame.Color(Chip.ColorsOfFigures.LIGHT_GREEN),
            pygame.Color(Chip.ColorsOfFigures.CONIFERS),
            pygame.Color(Chip.ColorsOfFigures.BLUE))

        for figure in Chip.Figures:
            for color_of_figure in colors_of_figure:
                chip = Chip(figure, color_of_figure)

                self.__content.append(chip)
                self.__content.append(chip)
                self.__content.append(chip)

        shuffle(self.__content)

    def is_empty(self) -> bool:
        """
        возвращает значение 'истина', если "куча"
        пуста, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return len(self.__content) == 0

    def n_chips(self) -> int:
        """
        возвращает количество фишек в "куче".
        :return: количество фишек в "куче".
        """

        return len(self.__content)

    def give_chips(self, n_chips: int) -> list[Chip] | None:
        """
        выдаёт фишки из "кучи", если она не пуста.
        :param n_chips: количество запрашиваемых
        фишек.
        :return: фишки из "кучи" или None.
        """

        validate_int_value(
            n_chips,
            (self.GIVE_CHIPS_PARAMETER_MIN_VALUE,
             Deck.N_CHIPS_MAX_VALUE))

        if not self.is_empty():
            given_chips = []

            n_given_chips = min(n_chips, len(self.__content))

            for i in range(n_given_chips):
                given_chip_index = randint(0, len(self.__content) - 1)

                given_chip = self.__content[given_chip_index]

                self.__content.pop(given_chip_index)

                given_chips.append(given_chip)

            shuffle(given_chips)

            return given_chips
        else:
            return None

    def return_chips(
            self,
            returned_chips: list[Chip]) -> None:
        """
        возвращает фишки в "кучу".
        :param returned_chips: возвращаемые в "кучу" фишки.
        """

        validate_container_elements_type(returned_chips, Chip)

        self.__content += returned_chips

        shuffle(self.__content)

    def make_an_exchange_of_chips(
            self,
            returned_chips: list[Chip]) -> list[Chip] | Chip | None:
        """
        производит обмен фишек, выдавая новые взамен возвращаемых
        (если "куча" пуста, обмен не производится, возвращается
        None).
        :param returned_chips: возвращаемый объект (фишка или
        колода фишек).
        :return: новая объект, выданный взамен возвращаемого,
        или None.
        """

        validate_container_elements_type(returned_chips, Chip)

        if not self.is_empty():
            new_chips = self.give_chips(len(returned_chips))

            while len(new_chips) < len(returned_chips):
                returned_chips.pop(-1)

            self.return_chips(returned_chips)

            if len(new_chips) == 1:
                return new_chips[0]
            else:
                return new_chips
        else:
            return returned_chips
