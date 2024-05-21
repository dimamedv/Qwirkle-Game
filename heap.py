from chip import Chip

import pygame

from random import shuffle, randint


# класс "куча (набор фишек)".
class Heap:
    def __init__(self):
        """
        конструктор класса.
        """

        self.content = []

        colors_of_figure = (pygame.Color(Chip.ColorsOfFigures.RED),
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

    def give_chip(self) -> Chip:
        """
        выдаёт фишку из "кучи".
        :return: фишка из "кучи".
        """

        chip_index = randint(0, len(self.content) - 1)

        chip = self.content[chip_index]

        self.content.pop(chip_index)

        return chip

    def __return_chip(self, returned_chip: Chip) -> None:
        """
        возвращает фишку в "кучу" и перемешивает
        её.
        :param returned_chip: возвращаемая в "кучу"
        фишка.
        """

        self.content.append(returned_chip)

        shuffle(self.content)

    def make_an_exchange_of_chip(
            self,
            returned_chip: Chip) -> [Chip, None]:
        """
        производит обмен фишки, выдавая новую фишку
        взамен возвращаемой (если "куча" пуста, обмен
        не производится, возвращается None).
        :param returned_chip: фишка, возвращаемая в "кучу",
        если "куча" не пуста.
        :return: новая фишка, выданная взамен возвращаемой,
        или None.
        """

        if not self.__is_empty():
            new_chip = self.give_chip()

            self.__return_chip(returned_chip)

            return new_chip
        else:
            return None
