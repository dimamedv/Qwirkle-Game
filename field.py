import enum


# класс "игровое поле".
class Field:
    # перечисление "константы игрового поля".
    class Constants(enum.IntEnum):
        # ширина сетки игрового поля;
        GRID_WIDTH = 15

        # высота сетки игрового поля;
        GRID_HEIGHT = 15

    def __init__(self,
                 content=None,
                 last_choice=None,
                 n_laid_out_chips=0):
        """
        конструктор класса.
        :param content: содержимое игрового поля;
        :param last_choice: индексы строки и столбца
        последней клетки игрового поля, в которую
        пользователь хотел поместить фишку;
        :param n_laid_out_chips: количество выложенных
        на поле фишек.
        """

        self.content = \
            [[None for _ in range(self.Constants.GRID_WIDTH)]
             for _ in range(self.Constants.GRID_HEIGHT)] if content is None else content

        if last_choice is None:
            self.reset_last_choice()
        else:
            self.last_choice = last_choice

        self.n_laid_out_chips = n_laid_out_chips if n_laid_out_chips != 0 else 0

    def copy(self, copy_last_choice=False):
        """
        возвращает копию игрового поля.
        :param copy_last_choice: флаг, указывающий,
        копировать поле last_choice или нет;
        :return: копия игрового поля.
        """

        last_choice_to_copy = self.last_choice if copy_last_choice else None

        return Field(self.content, last_choice_to_copy, self.n_laid_out_chips)

    def set_last_choice(self, last_choice):
        """
        устанавливает новое значение для
        поля last_choice.
        :param last_choice: .
        """

        self.last_choice = last_choice

    def reset_last_choice(self):
        """
        устанавливает значение по умолчанию
        для поля last_choice.
        """

        self.last_choice = (-1, -1)

    def validate_cell_indexes(self, cell_indexes):
        """
        производит валидацию входных индексов строки
        и столбца сетки игрового поля.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        if cell_indexes[0] < 0 or cell_indexes[0] >= self.Constants.GRID_HEIGHT:
            raise ValueError("invalid value of row_index")
        elif cell_indexes[1] < 0 or cell_indexes[1] >= self.Constants.GRID_WIDTH:
            raise ValueError("invalid value of column_index")

    def place_chip(self, chip, cell_indexes):
        """
        помещает фишку на игровое поле.
        :param chip: объект фишки;
        :param cell_indexes: индексы строки и
        столбца клетки игрового поля.
        """

        self.validate_cell_indexes(cell_indexes)

        self.content[cell_indexes[0]][cell_indexes[1]] = chip
        self.n_laid_out_chips += 1

    def remove_chip(self, cell_indexes):
        """
        удаляет фишку с игрового поля.
        :param cell_indexes: индексы строки
        и столбца клетки игрового поля.
        """

        self.validate_cell_indexes(cell_indexes)

        self.content[cell_indexes[0]][cell_indexes[1]] = None
        self.n_laid_out_chips -= 1

    def get_content_of_cell(self, cell_indexes):
        """
        возвращает содержимое клетки игрового поля.
        (фишку или None).
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля;
        :return: содержимое клетки игрового поля.
        """

        self.validate_cell_indexes(cell_indexes)

        return self.content[cell_indexes[0]][cell_indexes[1]]

    def has_chip_in_this_cell(self, cell_indexes):
        """
        возвращает значение 'истина', если в клетке
        игрового поля расположена фишка, в противном
        случае - 'ложь'.
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля;
        :return: 'истина' или 'ложь'.
        """

        self.validate_cell_indexes(cell_indexes)

        return self.get_content_of_cell(cell_indexes) is not None

    def has_only_one_chip(self):
        """
        возвращает значение 'истина', если
        на игровом поле находится только одна
        одна фишка, в противном случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return self.n_laid_out_chips == 1

    def has_at_least_one_neighboring_chip_to_this_chip(
            self,
            cell_indexes):
        """
        возвращает значение 'истина', если на игровом поле
        расположена фишка, являющееся соседней к рассматриваемой
        (соседная фишка, фишка расположенная выше, ниже, левее
        или правее рассматриваемой)
        :param cell_indexes: индексы строки и столбца
        клетки игрового поля.
        """

        self.validate_cell_indexes(cell_indexes)

        if self.n_laid_out_chips == 0:
            return False

        n_neighboring_chips = 0

        if cell_indexes[0] > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0] - 1, cell_indexes[1]))

        if cell_indexes[1] > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0], cell_indexes[1] - 1))

        if cell_indexes[0] < self.Constants.GRID_HEIGHT:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0] + 1, cell_indexes[1]))

        if cell_indexes[1] < self.Constants.GRID_WIDTH:
            n_neighboring_chips += self.has_chip_in_this_cell(
                (cell_indexes[0], cell_indexes[1] + 1))

        return n_neighboring_chips != 0

    def is_correct_last_choice(self):
        """
        возвращает значение 'истина', если
        выбор пользователем клетки поля для
        размещения фишки является корректным
        с точки зрения правил игры, в противном
        случае - 'ложь'.
        :return: 'истина' или 'ложь'.
        """

        return (self.has_only_one_chip() or
                self.has_at_least_one_neighboring_chip_to_this_chip(self.last_choice))
