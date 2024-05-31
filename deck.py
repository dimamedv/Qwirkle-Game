from validators import *
from chip import Chip

import pygame
from copy import copy
from collections import defaultdict


# класс "колода фишек".
class Deck:
    N_CHIPS_MIN_VALUE = 0

    N_CHIPS_MAX_VALUE = 6

    CHIP_INDEX_MIN_VALUE = N_CHIPS_MIN_VALUE

    CHIP_INDEX_MAX_VALUE = N_CHIPS_MAX_VALUE - 1

    CONTENT_MIN_SIZE = 1

    CONTENT_MAX_SIZE = N_CHIPS_MAX_VALUE

    def __init__(self, content: list[Chip] | None = None) -> None:
        """
        конструктор класса.
        """

        self.__content = []

        self.__n_chips = 0

        if content is not None:
            validate_int_value(
                len(content),
                (self.N_CHIPS_MAX_VALUE, None))

            validate_container_elements_type(content, Chip)

            for i in range(self.N_CHIPS_MAX_VALUE):
                self.__content.append(None)

            self.place_chips(content)

    @property
    def is_empty(self) -> bool:
        """
        возвращает значение 'истина', если колода
        фишек пуста, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.__n_chips == 0

    @property
    def is_full(self) -> bool:
        """
        возвращает значение 'истина', если колода
        фишек полна, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.__n_chips == self.N_CHIPS_MAX_VALUE

    @property
    def content(self) -> list[Chip | None]:
        """
        возвращает содержимое колоды фишек.
        :return: содержимое колоды фишек.
        """

        return self.__content

    @property
    def chips_set(self) -> set[Chip]:
        """
        возвращает множество фишек колоды.
        :return: множество фишек колоды.
        """

        chips_set = set()

        for chip in self.__content:
            if chip is not None:
                chips_set.add(chip)

        return chips_set

    def place_chip(self,
                   chip: Chip,
                   chip_index: int) -> None:
        """
        помещает фишку в колоду.
        :param chip: фишка, которая помещается в колоду.
        :param chip_index: индекс помещаемой фишки.
        """

        validate_object_type(chip, Chip)

        validate_int_value(
            chip_index,
            (self.CHIP_INDEX_MIN_VALUE,
             self.CHIP_INDEX_MAX_VALUE))

        old_chip = copy(self.__content[chip_index])

        self.__content[chip_index] = chip

        self.__n_chips += old_chip is None

    def remove_chip(self, chip_index: int) -> None:
        """
        убирает фишку из колоды.
        :param chip_index: индекс убираемой фишки.
        """

        validate_int_value(
            chip_index,
            (self.CHIP_INDEX_MIN_VALUE,
             self.CHIP_INDEX_MAX_VALUE))

        if self.__content[chip_index] is not None:
            self.__content[chip_index] = None

            self.__n_chips -= 1

    def place_chips(self, content: list) -> None:
        """
        помещает фишки в колоду.
        :param content: помещаемые в колоду фишки.
        """

        validate_int_value(
            len(content),
            (self.CONTENT_MIN_SIZE, self.CONTENT_MAX_SIZE))

        validate_container_elements_type(content, Chip)

        if self.N_CHIPS_MAX_VALUE - self.__n_chips == len(content):
            i = 0

            for chip in content:
                self.__content[i] = chip

                i += 1

            self.__n_chips += len(content)

    def place_on_places(
            self,
            chips: list[Chip],
            places_indexes: list[int]) -> list[Chip]:
        """
        помещает фишки на определенные места в колоде.
        :param chips: помещаемые в колоду фишки.
        :param places_indexes: индексы мест в колоде.
        :return: содержимое колоды фишек на определенных
        местах.
        """

        validate_container_elements_type(chips, Chip)
        validate_container_elements_type(places_indexes, int)

        validate_equality(len(chips), len(places_indexes))

        i = 0
        for place_index in places_indexes:
            validate_int_value(
                place_index,
                (self.CHIP_INDEX_MIN_VALUE, self.CHIP_INDEX_MAX_VALUE))

            self.__content[place_index] = chips[i]

            self.__n_chips += 1

            i += 1

    def replenish(self, new_chips: list[Chip]) -> list[Chip]:
        """
        восполняет колоду новыми фишками и возвращает лишние.
        :param new_chips: новые фишки.
        :return: лишние фишки.
        """

        validate_container_elements_type(new_chips, Chip)

        if not self.is_full:
            for i in range(self.N_CHIPS_MAX_VALUE):
                chip = self.__content[i]

                if chip is None and new_chips:
                    self.place_chip(new_chips[0], i)

                    new_chips.pop(0)

            return new_chips
        else:
            return new_chips

    def empty_out(self) -> None:
        """
        опустошает колоду фишек.
        """

        for i in range(self.N_CHIPS_MAX_VALUE):
            self.__content[i] = None

        self.__n_chips = 0

    def chip(self, chip_index: int) -> Chip | None:
        """
        возвращает фишку из колоды по её индексу.
        :param chip_index: индекс фишки в колоде.
        :return: фишка из колоды.
        """

        validate_int_value(
            chip_index,
            (self.CHIP_INDEX_MIN_VALUE,
             self.CHIP_INDEX_MAX_VALUE))

        return self.__content[chip_index]

    def content_on_places(
            self,
            places_indexes: list[int]) -> list[Chip | None]:
        """
        возвращает содержимое колоды фишек на определенных
        местах.
        :param places_indexes: индексы мест в колоде.
        :return: содержимое колоды фишек на определенных
        местах.
        """

        validate_container_elements_type(places_indexes, int)

        content_on_places = []

        for place_index in places_indexes:
            validate_int_value(
                place_index,
                (self.CHIP_INDEX_MIN_VALUE, self.CHIP_INDEX_MAX_VALUE))

            content_on_places.append(self.__content[place_index])

        return content_on_places

    @property
    def empty_places_for_chips_indexes(self) -> list[int]:
        """
        возвращает индексы не занятых фишками мест колоды.
        :return: индексы не занятых фишками мест колоды.
        """

        empty_places_for_chips_indexes = []

        for i in range(self.N_CHIPS_MAX_VALUE):
            if self.__content[i] is None:
                empty_places_for_chips_indexes.append(i)

        return empty_places_for_chips_indexes

    @property
    def non_empty_places_for_chips_indexes(self) -> list[int]:
        """
        возвращает индексы занятых фишками мест колоды.
        :return: индексы занятых фишками мест колоды.
        """

        non_empty_places_for_chips_indexes = []

        for i in range(self.N_CHIPS_MAX_VALUE):
            if isinstance(self.__content[i], Chip):
                non_empty_places_for_chips_indexes.append(i)

        return non_empty_places_for_chips_indexes

    @staticmethod
    def max_n_of_same_type_chips(
            chips_property: list[int] | list[pygame.Color]) -> int:
        """
        возвращает максимальное количество однотипных по свойству
        фишек в колоде.
        :param chips_property: значения свойства фишек.
        :return: максимальное количество однотипных по свойству
        фишек в колоде.
        """

        max_n = 1

        for i in range(len(chips_property)):
            n_for_current_chip = 1

            for j in range(i + 1, len(chips_property)):
                n_for_current_chip += chips_property[i] == chips_property[j]

                max_n = max(n_for_current_chip, max_n)

        return max_n

    @property
    def max_n_of_same_by_color_or_figure_chips(self) -> int:
        """
        возвращает максимальное количество фишек
        одного цвета или одной формы в колоде.
        :return: максимальное количество фишек
        одного цвета или одной формы в колоде.
        """

        validate_container_elements_type(self.__content, Chip)

        validate_int_value(
            self.__n_chips,
            (self.N_CHIPS_MAX_VALUE, None))

        figures = [chip.figure for chip in self.chips_set]
        colors_of_figures = [chip.color_of_figure for chip in self.chips_set]

        return max(self.max_n_of_same_type_chips(figures),
                   self.max_n_of_same_type_chips(colors_of_figures))

    def get_chips_by_property_value(
            self,
            property_value) -> list[Chip]:
        """
        возвращает фишки колоды, соответствующие
        признаку.
        :param property_value: требуемый признак
        (цвет или форма фигуры).
        :return: фишки колоды, соответствующие
        признаку.
        """

        chips = []

        for item in self.__content:
            if isinstance(item, Chip):
                if ((isinstance(property_value, int) and
                     item.figure == property_value) or
                        (isinstance(property_value, pygame.Color) and
                         item.color_of_figure == property_value)):
                    chips.append(item)

        return chips
