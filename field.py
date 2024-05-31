from chip import Chip
from deck import Deck

from copy import copy


# класс "игровое поле".
class Field:
    DISPLAYED_PART_N_CELLS_IN_WIDTH = 15

    DISPLAYED_PART_N_CELLS_IN_HEIGHT = DISPLAYED_PART_N_CELLS_IN_WIDTH

    N_LAID_OUT_CHIPS_MAX_VALUE = 108

    N_CELLS_IN_WIDTH = \
        (2 * (N_LAID_OUT_CHIPS_MAX_VALUE - 1) +
         DISPLAYED_PART_N_CELLS_IN_WIDTH)

    N_CELLS_IN_HEIGHT = N_CELLS_IN_WIDTH

    CELL_ROW_INDEX_SHIFT_INIT_VALUE = 107

    CELL_COLUMN_INDEX_SHIFT_INIT_VALUE = \
        CELL_ROW_INDEX_SHIFT_INIT_VALUE

    CELL_INDEX_SHIFT_MAX_VALUE = N_CELLS_IN_WIDTH - DISPLAYED_PART_N_CELLS_IN_WIDTH

    LAST_CHOICE_INIT_VALUE = (-1, -1)

    SHIFT_DISPLAYED_PART_UP = 0

    SHIFT_DISPLAYED_PART_DOWN = 1

    SHIFT_DISPLAYED_PART_LEFT = 2

    SHIFT_DISPLAYED_PART_RIGHT = 3

    LINE_OF_CHIPS_MAX_LENGTH = 6

    VERTICAL_LINE_OF_CHIPS = 0

    HORIZONTAL_LINE_OF_CHIPS = 1

    CYCLE_OF_LINE_BEGINNING_SEARCH = 0

    CYCLE_OF_LINE_ENDING_SEARCH = 0

    def __init__(self,
                 content: list[list[Chip, None]] = None,
                 last_choice: tuple[int, int] = None,
                 n_laid_out_chips: int = None,
                 cell_row_index_shift: int = None,
                 cell_column_index_shift: int = None,
                 min_max_cell_indexes: tuple[int, int, int, int] = None) -> None:
        """
        конструктор класса.
        :param content: содержимое игрового поля.
        :param last_choice: индексы строки и столбца
        последней клетки игрового поля, в которую
        пользователь хотел поместить фишку.
        :param n_laid_out_chips: количество выложенных
        на поле фишек.
        :param cell_row_index_shift: сдвиг индекса строки
        клетки.
        :param cell_column_index_shift: сдвиг индекса строки
        клетки.
        :param min_max_cell_indexes: минимальные и максимальные
        индексы клеток фишек.
        """

        self.__content = \
            [[None for _ in range(self.N_CELLS_IN_WIDTH)]
             for _ in range(self.N_CELLS_IN_HEIGHT)] if content is None else content

        if last_choice is None:
            self.__last_choice = None

            self.reset_last_choice()
        else:
            self.__last_choice = last_choice

        self.__n_put_up_chips = n_laid_out_chips if n_laid_out_chips else 0

        if cell_row_index_shift is None:
            self.reset_cell_row_index_shift()
        else:
            self.__cell_row_index_shift = cell_row_index_shift

        if cell_column_index_shift is None:
            self.reset_cell_column_index_shift()
        else:
            self.__cell_column_index_shift = cell_column_index_shift

        if min_max_cell_indexes is not None:
            self.__min_cell_row_index = min_max_cell_indexes[0]
            self.__min_cell_column_index = min_max_cell_indexes[1]

            self.__max_cell_row_index = min_max_cell_indexes[2]
            self.__max_cell_column_index = min_max_cell_indexes[3]
        else:
            self.__min_cell_row_index = self.N_CELLS_IN_HEIGHT
            self.__min_cell_column_index = self.N_CELLS_IN_WIDTH

            self.__max_cell_row_index = -1
            self.__max_cell_column_index = -1

    def copy(self,
             copy_last_choice: bool = False):
        """
        возвращает копию игрового поля.
        :param copy_last_choice: флаг, указывающий,
        копировать поле last_choice или нет.
        :return: копия игрового поля.
        """

        last_choice_to_copy = \
            self.__last_choice if copy_last_choice else None

        return Field(copy(self.__content),
                     last_choice_to_copy,
                     copy(self.__n_put_up_chips),
                     copy(self.__cell_row_index_shift),
                     copy(self.__cell_column_index_shift),
                     (copy(self.__min_cell_row_index),
                      copy(self.__min_cell_column_index),
                      copy(self.__max_cell_row_index),
                      copy(self.__max_cell_column_index)))

    @property
    def n_put_up_chips(self) -> int:
        """
        возвращает значение поля __n_put_up_chips.
        :return: значение поля __n_put_up_chips.
        """

        return self.__n_put_up_chips

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

        if self.__last_choice is not None:
            self.__min_cell_row_index = min(
                self.__last_choice[0],
                self.__min_cell_row_index)

            self.__min_cell_column_index = min(
                self.__last_choice[1],
                self.__min_cell_column_index)

            self.__max_cell_row_index = max(
                self.__last_choice[0],
                self.__max_cell_row_index)

            self.__max_cell_column_index = max(
                self.__last_choice[1],
                self.__max_cell_column_index)

        self.__last_choice = self.LAST_CHOICE_INIT_VALUE

    def has_last_choice_init_value(self) -> bool:
        """
        возвращает значение 'истина', если поле
        __last_choice имеет значение по умолчанию,
        в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.__last_choice == self.LAST_CHOICE_INIT_VALUE

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
        поля __cell_row_index_shift.
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
        поля __cell_row_index_shift.
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
            cell_indexes: tuple[int, int],
            is_necessary_to_validate_last_choice: bool = False) -> None:
        """
        производит валидацию входных индексов строки
        и столбца сетки игрового поля.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        if is_necessary_to_validate_last_choice:
            left_border = -1
        else:
            left_border = 0

        if (cell_indexes[0] < left_border or
                cell_indexes[0] >= self.N_CELLS_IN_HEIGHT):
            raise ValueError("invalid value of row_index")
        elif (cell_indexes[1] < left_border or
              cell_indexes[1] >= self.N_CELLS_IN_WIDTH):
            raise ValueError("invalid value of column_index")

    def place_chip(
            self,
            chip: Chip,
            cell_indexes: tuple[int, int]) -> None:
        """
        помещает фишку на игровое поле.
        :param chip: объект фишки.
        :param cell_indexes: индексы строки и
        столбца клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        self.__content[cell_indexes[0]][cell_indexes[1]] = chip
        self.__n_put_up_chips += 1

    def remove_chip(self,
                    cell_indexes: tuple[int, int]) -> None:
        """
        удаляет фишку с игрового поля.
        :param cell_indexes: индексы строки
        и столбца клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        self.__content[cell_indexes[0]][cell_indexes[1]] = None
        self.__n_put_up_chips -= 1

    def get_content_of_cell(
            self,
            cell_indexes: tuple[int, int]) -> [Chip, None]:
        """
        возвращает содержимое клетки игрового поля.
        (фишку или None).
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        :return: содержимое клетки игрового поля.
        """

        self.__validate_cell_indexes(
            cell_indexes,
            is_necessary_to_validate_last_choice=True)

        if cell_indexes == self.LAST_CHOICE_INIT_VALUE:
            return None
        else:
            return self.__content[cell_indexes[0]][cell_indexes[1]]

    def has_chip_in_this_cell(
            self,
            cell_indexes: tuple[int, int]) -> bool:
        """
        возвращает значение 'истина', если в клетке
        игрового поля расположена фишка, в противном
        случае - 'ложь'.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        :return: 'истина' или 'ложь'.
        """

        self.__validate_cell_indexes(
            cell_indexes,
            is_necessary_to_validate_last_choice=True)

        return isinstance(self.get_content_of_cell(cell_indexes), Chip)

    def has_only_one_chip(self) -> bool:
        """
        возвращает значение 'истина', если
        на игровом поле находится только одна
        одна фишка, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.__n_put_up_chips == 1

    def __is_correct_cell_index_for_chips_line_cycle(
            self,
            cell_indexes: tuple[int, int],
            type_of_chips_line: int,
            type_of_cycle: int) -> bool:
        """
        возвращает значение логического выражения для
        проверки условия цикла, обрабатывающего линию
        фишек на игровом поле.
        :param cell_indexes: индексы строки и столбца
        рассматриваемой клетки игрового поля.
        :param type_of_chips_line: тип линии.
        :param type_of_cycle: тип цикла.
        :return: 'истина' или 'ложь'.
        """

        match type_of_chips_line, type_of_cycle:
            case self.VERTICAL_LINE_OF_CHIPS, self.CYCLE_OF_LINE_BEGINNING_SEARCH:
                return cell_indexes[0] > 0
            case self.VERTICAL_LINE_OF_CHIPS, self.CYCLE_OF_LINE_ENDING_SEARCH:
                return cell_indexes[0] < self.N_CELLS_IN_HEIGHT
            case self.HORIZONTAL_LINE_OF_CHIPS, self.CYCLE_OF_LINE_BEGINNING_SEARCH:
                return cell_indexes[1] > 0
            case self.HORIZONTAL_LINE_OF_CHIPS, self.CYCLE_OF_LINE_ENDING_SEARCH:
                return cell_indexes[1] < self.N_CELLS_IN_WIDTH

    def __get_cell_indexes_of_chips_line_beginning(
            self,
            cell_indexes: tuple[int, int],
            cell_indexes_deltas: tuple[int, int],
            type_of_chips_line: int) -> tuple[int, int]:
        """
        возвращает индексы строки и столбца клетки игрового
        поля, с которой начинается линия фишек.
        :param cell_indexes: индексы строки и столбца клетки
        игрового поля, с которой начинается поиск начала линии
        фишек.
        :param cell_indexes_deltas: значения шага изменения
        индексо строки и столбца клетки для поиска.
        :param type_of_chips_line: тип линии фишек (вертикальный
        или горизонтальный).
        :return: индексы строки и столбца клетки игрового
        поля, с которой начинается линия фишек.
        """

        cell_row_index = cell_indexes[0] - cell_indexes_deltas[0]
        cell_column_index = cell_indexes[1] - cell_indexes_deltas[1]

        line_length = 0

        while (self.__is_correct_cell_index_for_chips_line_cycle(
                (cell_row_index, cell_column_index),
                type_of_chips_line,
                self.CYCLE_OF_LINE_BEGINNING_SEARCH) and
               self.has_chip_in_this_cell(
                   (cell_row_index, cell_column_index))):
            line_length += 1

            if line_length == self.LINE_OF_CHIPS_MAX_LENGTH:
                return -1, -1

            cell_row_index -= cell_indexes_deltas[0]
            cell_column_index -= cell_indexes_deltas[1]

        cell_row_index += cell_indexes_deltas[0]
        cell_column_index += cell_indexes_deltas[1]

        return cell_row_index, cell_column_index

    def __get_parameters_of_processed_line(
            self,
            cell_indexes: tuple[int, int],
            cell_indexes_deltas: tuple[int, int],
            type_of_chips_line: int) -> tuple[bool, int]:
        """
        возвращает параметры обработанной линии фишек.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля, с которой начинается обработка
        линии фишек.
        :param cell_indexes_deltas: значения шага изменения
        индексо строки и столбца клетки для поиска.
        :param type_of_chips_line: тип линии фишек (вертикальный
        или горизонтальный).
        :return: параметры обработанной линии фишек (будет ли
        она соответствовать правилам игры после добавления 
        фишки, а также новая количество фишек в линии).
        """

        this_chip = self.get_content_of_cell(cell_indexes)

        chips_set = set()
        chips_set.add(this_chip)

        figures_set = set()
        figures_set.add(this_chip.figure)

        colors_of_figures_set = set()
        colors_of_figures_set.add(this_chip.color_of_figure_tuple)

        cell_row_index = cell_indexes[0]
        cell_column_index = cell_indexes[1]

        line_length = 0

        while (self.__is_correct_cell_index_for_chips_line_cycle(
                (cell_row_index, cell_column_index),
                type_of_chips_line,
                self.CYCLE_OF_LINE_ENDING_SEARCH) and
               self.has_chip_in_this_cell(
                   (cell_row_index, cell_column_index))):
            line_length += 1

            if line_length > self.LINE_OF_CHIPS_MAX_LENGTH:
                return False, -1

            chip = self.get_content_of_cell((cell_row_index,
                                             cell_column_index))

            chips_set.add(chip)

            figures_set.add(chip.figure)
            colors_of_figures_set.add(chip.color_of_figure_tuple)

            cell_row_index += cell_indexes_deltas[0]
            cell_column_index += cell_indexes_deltas[1]

        if (line_length == 1 or
                (len(chips_set) == line_length and
                 (len(figures_set) == 1) != (len(colors_of_figures_set) == 1))):
            return True, line_length
        else:
            return False, line_length

    def __will_line_correct_with_this_chip(
            self,
            cell_indexes: tuple[int, int],
            type_of_chips_line: int) -> tuple[bool, int]:
        """
        возвращает значение 'истина', если линия
        (вертикальная или горизонтальная) будет
        корректной с точки зрения правил игры
        с добавлением рассматриваемой фишки,
        в противном случае - 'ложь'.
        :param cell_indexes: индексы строки и
        столбца клетки игрового поля рассматриваемой
        фишки.
        :param type_of_chips_line: тип линии фишек
        (горизонтальная или вертикальная).
        :return: 'истина' или 'ложь'.
        """

        cell_row_index_delta = 0
        cell_column_index_delta = 0

        match type_of_chips_line:
            case self.VERTICAL_LINE_OF_CHIPS:
                cell_row_index_delta = 1
            case self.HORIZONTAL_LINE_OF_CHIPS:
                cell_column_index_delta = 1

        cell_indexes_deltas = (cell_row_index_delta, cell_column_index_delta)

        current_cell_indexes = \
            self.__get_cell_indexes_of_chips_line_beginning(
                cell_indexes,
                cell_indexes_deltas,
                type_of_chips_line)

        if current_cell_indexes == self.LAST_CHOICE_INIT_VALUE:
            return False, -1

        return self.__get_parameters_of_processed_line(
            current_cell_indexes,
            cell_indexes_deltas,
            type_of_chips_line)

    def is_last_choice_correct_in_the_context_of_chips_lines(
            self,
            cell_indexes: tuple[int, int]) -> tuple[bool, int]:
        """
        возвращает значение 'истина', если выбор пользователем
        клетки поля для размещения фишки является корректным
        в разрезе линий фишек, в противном случае - 'ложь'.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        self.__validate_cell_indexes(cell_indexes)

        (will_vertical_line_correct,
         vertical_line_new_length) = \
            self.__will_line_correct_with_this_chip(
                cell_indexes,
                self.VERTICAL_LINE_OF_CHIPS)

        (will_horizontal_line_correct,
         horizontal_line_new_length) = \
            self.__will_line_correct_with_this_chip(
                cell_indexes,
                self.HORIZONTAL_LINE_OF_CHIPS)

        if (vertical_line_new_length == 1 and
                horizontal_line_new_length == 1):
            points = 0
        else:
            vertical_line_points = vertical_line_new_length

            if vertical_line_new_length == 6:
                vertical_line_points += 6
            elif vertical_line_new_length <= 1:
                vertical_line_points = 0

            horizontal_line_points = horizontal_line_new_length

            if horizontal_line_new_length == 6:
                horizontal_line_points += 6
            elif horizontal_line_points <= 1:
                horizontal_line_points = 0

            points = vertical_line_points + horizontal_line_points

        return \
            (((will_vertical_line_correct and
               will_horizontal_line_correct and
               (vertical_line_new_length + horizontal_line_new_length) > 2)),
             points)

    def is_last_choice_correct(self) -> bool:
        """
        возвращает значение 'истина', если
        выбор пользователем клетки поля для
        размещения фишки является корректным
        с точки зрения правил игры, в противном
        случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return \
            (not self.has_last_choice_init_value() and
             (self.has_only_one_chip() or
              self.is_last_choice_correct_in_the_context_of_chips_lines(
                  self.__last_choice)[0]))

    def shift_displayed_part(self,
                             direction: int) -> None:
        """
        сдвигает отображаемую область игрового поля на
        одну клетку в указанном направлении.
        :param direction: направление, в котором будет
        сдвинута отображаемая область поля.
        """

        if direction not in (self.SHIFT_DISPLAYED_PART_UP,
                             self.SHIFT_DISPLAYED_PART_DOWN,
                             self.SHIFT_DISPLAYED_PART_LEFT,
                             self.SHIFT_DISPLAYED_PART_RIGHT):
            raise ValueError("there is no such direction for shift")

        match direction:
            case self.SHIFT_DISPLAYED_PART_UP:
                self.cell_row_index_shift -= self.cell_row_index_shift > 0
            case self.SHIFT_DISPLAYED_PART_DOWN:
                self.cell_row_index_shift += \
                    self.cell_row_index_shift < self.CELL_INDEX_SHIFT_MAX_VALUE
            case self.SHIFT_DISPLAYED_PART_LEFT:
                self.cell_column_index_shift -= self.cell_column_index_shift > 0
            case self.SHIFT_DISPLAYED_PART_RIGHT:
                self.cell_column_index_shift += \
                    self.cell_column_index_shift < self.CELL_INDEX_SHIFT_MAX_VALUE

    def replace_last_choice_chip(self,
                                 new_chip: Chip) -> None:
        """
        заменяет фишку, для которой предварительно
        выбрана клетка на игровом поле, на новую.
        :param new_chip: новая фишка.
        """

        if (new_chip is not None and
                not self.has_last_choice_init_value()):
            self.__content[self.__last_choice[0]][self.__last_choice[1]] = new_chip

    def is_deck_useless(self, deck_content: list[Chip]) -> bool:
        """
        возвращает значение 'истина', если ни одну
        из фишек колоды нельзя выставить на поле,
        в противном случае - 'ложь'.
        :param deck_content: фишки колоды.
        :return: 'истина' или 'ложь'.
        """

        if (len(deck_content) == 0 or
                self.n_put_up_chips == self.N_LAID_OUT_CHIPS_MAX_VALUE):
            return True

        if self.n_put_up_chips == 0:
            return False

        copy_of_field = self.copy()

        for element in deck_content:
            if isinstance(element, Chip):
                min_row_index = self.__min_cell_row_index
                min_row_index -= min_row_index > 0

                min_column_index = self.__min_cell_column_index
                min_column_index -= min_column_index > 0

                max_row_index = self.__max_cell_row_index
                max_row_index += max_row_index < self.N_CELLS_IN_HEIGHT

                max_column_index = self.__max_cell_column_index
                max_column_index += max_row_index < self.N_CELLS_IN_WIDTH

                for i in range(min_row_index, max_row_index + 1):
                    for j in range(min_column_index, max_column_index + 1):
                        if not isinstance(copy_of_field.get_content_of_cell((i, j)), Chip):
                            copy_of_field.place_chip(element, (i, j))
                            copy_of_field.last_choice = (i, j)

                            flag = copy_of_field.is_last_choice_correct()

                            copy_of_field.reset_last_choice()
                            copy_of_field.remove_chip((i, j))

                            if flag:
                                return False

        return True

    @property
    def min_max_cell_indexes(self) -> tuple[int, int, int, int]:
        """
        возвращает минимальные и максимальные значения
        индексов клеток, в которых расположены фишки.
        :return: минимальные и максимальные значения
        индексов клеток, в которых расположены фишки.
        """

        return \
            (self.__min_cell_row_index,
             self.__min_cell_column_index,
             self.__max_cell_row_index,
             self.__max_cell_column_index)

    def set_min_max_cell_indexes(
            self,
            indexes: tuple[int, int, int, int]) -> None:
        """
        устанавливает новые значения для минимальных и
        максимальных значений индексов клеток, в которых
        расположены фишки.
        :param indexes: новые значения.
        """

        self.__min_cell_row_index = indexes[0]
        self.__min_cell_column_index = indexes[1]
        self.__max_cell_row_index = indexes[2]
        self.__max_cell_column_index = indexes[3]
