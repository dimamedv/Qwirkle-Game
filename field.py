import enum


# класс "игровое поле".
class Field:
    # перечисление "константы игрового поля".
    class Constants(enum.IntEnum):
        # ширина сетки игрового поля;
        GRID_WIDTH = 14

        # высота сетки игрового поля;
        GRID_HEIGHT = 14

    def __init__(self):
        """
        конструктор класса.
        """

        self.data = [[None for _ in range(self.Constants.GRID_WIDTH)]
                     for _ in range(self.Constants.GRID_HEIGHT)]

    def validate_indexes(self, cell_row_index, cell_column_index):
        """
        производит валидацию входных индексов строки и
        столбца сетки игрового поля.
        :param cell_row_index: индекс строки клетки игрового
        поля;
        :param cell_column_index: индекс столбца клетки.
        """

        if cell_row_index < 0 or cell_row_index >= self.Constants.GRID_HEIGHT:
            raise ValueError("invalid value of row_index")
        elif cell_column_index < 0 or cell_column_index >= self.Constants.GRID_WIDTH:
            raise ValueError("invalid value of column_index")

    def place_chip(self, chip, cell_row_index, cell_column_index):
        """
        помещает фишку на игровое поле.
        :param chip: объект фишки;
        :param cell_row_index: индекс строки клетки игрового
        поля;
        :param cell_column_index: индекс столбца клетки.
        """

        self.validate_indexes(cell_row_index, cell_column_index)

        self.data[cell_row_index][cell_column_index] = chip

    def remove_chip(self, cell_row_index, cell_column_index):
        """
        удаляет фишку с игрового поля.
        :param cell_row_index: индекс строки клетки игрового
        поля;
        :param cell_column_index: индекс столбца клетки.
        """

        self.validate_indexes(cell_row_index, cell_column_index)

        self.data[cell_row_index][cell_column_index] = None

    def has_chip_in_this_cell(self, cell_row_index, cell_column_index):
        """
        возвращает значение 'истина', если в клетке игрового поля с индексом
        строки cell_row_index и индексом столбца cell_column_index расположена
        фишка, в противном случае - 'ложь'.
        :param cell_row_index: индекс строки клетки;
        :param cell_column_index: индекс столбца клетки.
        :return: 'истина' или 'ложь'.
        """

        self.validate_indexes(cell_row_index, cell_column_index)

        return self.data[cell_row_index][cell_column_index] is not None

    def get_content_of_cell(self, cell_row_index, cell_column_index):
        """
        возвращает содержимое клетки игрового поля
        :param cell_row_index: индекс строки клетки;
        :param cell_column_index: индекс столбца клетки.
        :return: объект фишки или None.
        """

        self.validate_indexes(cell_row_index, cell_column_index)

        return self.data[cell_row_index][cell_column_index]

    def has_at_least_one_neighboring_chip_to_this_chip(
            self,
            cell_row_index,
            cell_column_index):
        """
        возвращает значение 'истина', если на игровом поле
        расположена фишка, являющееся соседней к рассматриваемой
        (соседная фишка, фишка расположенная выше, ниже, левее
        или правее рассматриваемой)
        :param cell_row_index: индекс строки клетки в
        которой расположена фишка;
        :param cell_column_index: индекс столбца клетки в
        которой расположена фишка;
        """

        self.validate_indexes(cell_row_index, cell_column_index)

        n_neighboring_chips = 0

        if cell_row_index > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                cell_row_index - 1,
                cell_column_index)
        if cell_column_index > 0:
            n_neighboring_chips += self.has_chip_in_this_cell(
                cell_row_index,
                cell_column_index - 1)
        if cell_row_index < self.Constants.GRID_HEIGHT:
            n_neighboring_chips += self.has_chip_in_this_cell(
                cell_row_index + 1,
                cell_column_index)
        if cell_column_index < self.Constants.GRID_WIDTH:
            n_neighboring_chips += self.has_chip_in_this_cell(
                cell_row_index,
                cell_column_index + 1)

        return n_neighboring_chips != 0
