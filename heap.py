from chip import Chip
from deck import Deck

import pygame

from random import shuffle, randint


# класс "куча (набор фишек)".
class Heap:
    def __init__(self):
        """
        конструктор класса.
        """

        self.content = []

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

                self.content.append(chip)
                self.content.append(chip)
                self.content.append(chip)

        shuffle(self.content)

    def __is_empty(self) -> bool:
        """
        возвращает значение 'истина', если "куча"
        пуста, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return len(self.content) == 0

    def give_chips(self, n_chips: int) -> [list[Chip], None]:
        """
        выдаёт фишки из "кучи", если она не пуста
        :param n_chips: количество выдаваемых фишек.
        :return: колода карт из "кучи".
        """

        if n_chips < 0 or n_chips > Deck.N_CHIPS_MAX_VALUE:
            raise ValueError("invalid value of n_chips")

        if not self.__is_empty() and len(self.content) >= n_chips:
            chips = []

            for i in range(n_chips):
                chip_index = randint(0, len(self.content) - 1)

                chip = self.content[chip_index]

                self.content.pop(chip_index)

                chips.append(chip)

            shuffle(chips)

            return chips
        else:
            return None

    def __return_chips(self,
                       returned_chips: list[Chip]) -> None:
        """
        возвращает фишки в "кучу".
        :param returned_chips: возвращаемые в "кучу" фишки.
        """

        self.content.append(returned_chips)

        shuffle(self.content)

    def make_an_exchange_of_chips(
            self,
            returned_chips: list[Chip]) -> [list[Chip], None]:
        """
        производит обмен фишек, выдавая новые взамен возвращаемых
        (если "куча" пуста, обмен не производится, возвращается
        None).
        :param returned_chips: возвращаемый объект (фишка или
        колода фишек).
        :return: новая объект, выданный взамен возвращаемого,
        или None.
        """

        if not self.__is_empty():
            new_chips = self.give_chips(len(returned_chips))

            self.__return_chips(returned_chips)

            return new_chips
        else:
            return None
