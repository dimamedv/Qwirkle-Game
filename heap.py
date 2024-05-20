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

    def give_chip(self) -> Chip:
        """
        выдаёт фишку из кучи.
        :return: фишка из кучи.
        """

        chip_index = randint(0, len(self.content) - 1)

        chip = self.content[chip_index]

        self.content.pop(chip_index)

        return chip
