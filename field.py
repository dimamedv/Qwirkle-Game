from chip import Chip

import enum


# класс "игровое поле".
class Field:
    # количество клеток в ширину у отображаемой
    # на экране части сетки игрового поля.
    DISPLAYED_PART_N_CELLS_IN_WIDTH = 15

    # количество клеток в ширину у отображаемой
    # на экране части сетки игрового поля.
    DISPLAYED_PART_N_CELLS_IN_HEIGHT = DISPLAYED_PART_N_CELLS_IN_WIDTH

    # максимальное количество выложенных
    # на игровое поле фишек.
    N_LAID_OUT_CHIPS_MAX_VALUE = 108

    # количество клеток в ширину у сетки игрового поля.
    N_CELLS_IN_WIDTH = (2 * (N_LAID_OUT_CHIPS_MAX_VALUE - 1) +
                        DISPLAYED_PART_N_CELLS_IN_WIDTH)

    # количество клеток в ширину у сетки игрового поля.
    N_CELLS_IN_HEIGHT = N_CELLS_IN_WIDTH

    # сдвиг индекса строки клетки по умолчанию.
    CELL_ROW_INDEX_SHIFT_INIT_VALUE = 107

    # сдвиг индекса столбца клетки по умолчанию.
    CELL_COLUMN_INDEX_SHIFT_INIT_VALUE = 107

    def __init__(self,
                 content: list[list[Chip, None]] = None,
                 last_choice: tuple[int, int] = None,
                 n_laid_out_chips: int = None,
                 cell_row_index_shift: int = None,
                 cell_column_index_shift: int = None) -> None:
        """
        конструктор класса.
        :param content: содержимое игрового поля;
        :param last_choice: индексы строки и столбца
        последней клетки игрового поля, в которую
        пользователь хотел поместить фишку;
        :param n_laid_out_chips: количество выложенных
        на поле фишек.
        """

        self.__content = \
            [[None for _ in range(self.N_CELLS_IN_WIDTH)]
             for _ in range(self.N_CELLS_IN_HEIGHT)] if content is None else content

        if last_choice is None:
            self.reset_last_choice()
        else:
            self.__last_choice = last_choice

        self.__n_laid_out_chips = n_laid_out_chips if n_laid_out_chips else 0

        if cell_row_index_shift is None:
            self.reset_cell_row_index_shift()
        else:
            self.__cell_row_index_shift = cell_row_index_shift

        if cell_column_index_shift is None:
            self.reset_cell_column_index_shift()
        else:
            self.__cell_column_index_shift = cell_column_index_shift

    def copy(self,
             copy_last_choice: bool = False):
        """
        возвращает копию игрового поля.
        :param copy_last_choice: флаг, указывающий,
        копировать поле last_choice или нет;
        :return: копия игрового поля.
        """

        last_choice_to_copy = self.__last_choice if copy_last_choice else None

        return Field(self.__content,
                     last_choice_to_copy,
                     self.__n_laid_out_chips,
                     self.__cell_row_index_shift,
                     self.__cell_column_index_shift)

    @property
    def last_choice(self) -> tuple[int, int]:
        """
        возвращает значение поля __last_choice.
        :return: значение поля __last_choice.
        """

        return self.__last_choice

    @last_choice.setter
    def last_choice(
            self,
            last_choice_new_value: tuple[int, int]) -> None:
        """
        устанавливает новое значение поля __last_choice.
        :param last_choice_new_value: новое значение поля
        __last_choice.
        """

        self.__last_choice = last_choice_new_value

    def reset_last_choice(self) -> None:
        """
        устанавливает значение по умолчанию
        для поля __last_choice.
        """

        self.__last_choice = (-1, -1)

    @property
    def cell_row_index_shift(self) -> int:
        """
        возвращает значение поля __cell_row_index_shift.
        :return: значение поля __cell_row_index_shift.
        """

        return self.__cell_row_index_shift

    @cell_row_index_shift.setter
    def cell_row_index_shift(
            self,
            cell_row_index_shift_new_value: int) -> None:
        """
        устанавливает новое значение поля __cell_row_index_shift.
        :param cell_row_index_shift_new_value: новое значение
        поля __cell_row_index_shift..
        """

        self.__cell_row_index_shift = cell_row_index_shift_new_value

    def reset_cell_row_index_shift(self) -> None:
        """
        устанавливает значение по умолчанию
        для поля __cell_row_index_shift.
        """

        self.__cell_row_index_shift = self.CELL_ROW_INDEX_SHIFT_INIT_VALUE

    @property
    def cell_column_index_shift(self) -> int:
        """
        возвращает значение поля __cell_column_index_shift.
        :return: значение поля __cell_column_index_shift.
        """

        return self.__cell_column_index_shift

    @cell_column_index_shift.setter
    def cell_column_index_shift(
            self,
            cell_column_index_shift_new_value: int) -> None:
        """
        устанавливает новое значение поля __cell_row_index_shift.
        :param cell_column_index_shift_new_value: новое значение
        поля __cell_row_index_shift..
        """

        self.__cell_column_index_shift = cell_column_index_shift_new_value

    def reset_cell_column_index_shift(self) -> None:
        """
        устанавливает значение по умолчанию
        для поля __cell_column_index_shift.
        """

        self.__cell_column_index_shift = self.CELL_COLUMN_INDEX_SHIFT_INIT_VALUE

    def __validate_cell_indexes(
            self,
            cell_indexes: tuple[int, int]) -> None:
        """
        производит валидацию входных индексов строки
        и столбца сетки игрового поля.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        if cell_indexes[0] < 0 or cell_indexes[0] >= self.N_CELLS_IN_HEIGHT:
            raise ValueError("invalid value of row_index")
        elif cell_indexes[1] < 0 or cell_indexes[1] >= self.N_CELLS_IN_WIDTH:
            raise ValueError("invalid value of column_index")

    def place_chip(
            self,
            chip: Chip,
            cell_indexes: tuple[int, int]) -> None:
        """
        помещает фишку на игровое поле.
        :param chip: объект фишки;
        :param cell_indexes: индексы строки и
        столбца клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        self.__content[cell_indexes[0]][cell_indexes[1]] = chip
        self.__n_laid_out_chips += 1

    def remove_chip(self,
                    cell_indexes: tuple[int, int]) -> None:
        """
        удаляет фишку с игрового поля.
        :param cell_indexes: индексы строки
        и столбца клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        self.__content[cell_indexes[0]][cell_indexes[1]] = None
        self.__n_laid_out_chips -= 1

    def get_content_of_cell(
            self,
            cell_indexes: tuple[int, int]) -> [Chip, None]:
        """
        возвращает содержимое клетки игрового поля.
        (фишку или None).
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля;
        :return: содержимое клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        return self.__content[cell_indexes[0]][cell_indexes[1]]

    def has_chip_in_this_cell(
            self,
            cell_indexes: tuple[int, int]) -> bool:
        """
        возвращает значение 'истина', если в клетке
        игрового поля расположена фишка, в противном
        случае - 'ложь'.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля;
        :return: 'истина' или 'ложь'.
        """

        self.__validate_cell_indexes(cell_indexes)

        return self.get_content_of_cell(cell_indexes) is not None

    def has_only_one_chip(self) -> bool:
        """
        возвращает значение 'истина', если
        на игровом поле находится только одна
        одна фишка, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.__n_laid_out_chips == 1

    def has_at_least_one_neighboring_chip_to_this_chip(
            self,
            cell_indexes: tuple[int, int]) -> bool:
        """
        возвращает значение 'истина', если на игровом поле
        расположена фишка, являющееся соседней к рассматриваемой
        (соседная фишка, фишка расположенная выше, ниже, левее
        или правее рассматриваемой)
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        if self.__n_laid_out_chips == 0:
            return False

        n_neighboring_chips = 0

        if cell_indexes[0] > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0] - 1, cell_indexes[1]))

        if cell_indexes[1] > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0], cell_indexes[1] - 1))

        if cell_indexes[0] < self.DISPLAYED_PART_N_CELLS_IN_HEIGHT:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0] + 1, cell_indexes[1]))

        if cell_indexes[1] < self.DISPLAYED_PART_N_CELLS_IN_WIDTH:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0], cell_indexes[1] + 1))

        return n_neighboring_chips != 0

    def is_correct_last_choice(self) -> bool:
        """
        возвращает значение 'истина', если
        выбор пользователем клетки поля для
        размещения фишки является корректным
        с точки зрения правил игры, в противном
        случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return (self.has_only_one_chip() or
                self.has_at_least_one_neighboring_chip_to_this_chip(self.__last_choice))
