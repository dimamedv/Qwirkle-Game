from chip import Chip


# класс "колода фишек".
class Deck:
    # максимальное количество фишек в колоде.
    N_CHIPS_MAX_VALUE = 6

    def __init__(self, content: list[Chip]) -> None:
        """
        конструктор класса.
        """

        if len(content) != self.N_CHIPS_MAX_VALUE:
            raise ValueError("invalid value of content.")

        self.__content = []

        self.place_chips(content)

    def place_chips(self, chips: list) -> None:
        """
        помещает фишки в колоду, опустошая её.
        :param chips: помещаемые в колоду фишки.
        """

        self.empty_out()

        for chip in chips:
            self.__content.append(chip)

    def __is_empty(self) -> bool:
        """
        возвращает значение 'истина', если колода
        фишек пуста, в противном случае - 'ложь'.
        :return:
        """

        return not self.__content

    def chip(self, chip_index: int) -> [Chip, None]:
        """
        возвращает фишку из колоды по её индексу.
        :param chip_index: индекс фишки в колоде.
        :return: фишка из колоды.
        """

        return self.__content[chip_index]

    @property
    def content(self) -> list[Chip]:
        """
        возвращает содержимое колоды фишек.
        :return: содержимое колоды фишек.
        """

        return self.__content

    def empty_out(self) -> None:
        """
        опустошает колоду фишек.
        """

        self.__content.clear()

    def place_chip(self, chip, chip_index: int) -> None:
        """
        помещает фишку в колоду.
        :param chip: фишка, которая помещается в колоду
        :param chip_index: индекс помещаемой фишки.
        :return:
        """

        self.__content[chip_index] = chip

    def remove_chip(self, chip_index: int) -> None:
        """
        убирает фишку из колоды.
        :param chip_index: индекс убираемой фишки.
        """

        self.__content[chip_index] = None
