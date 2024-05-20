import enum
import pygame


# класс "фишка".
class Chip:
    # перечисление "фигуры, которые
    # могут быть нарисованы на игровой
    # фишке".
    class Figures(enum.IntEnum):
        # круг;
        CIRCLE = 0

        # квадрат;
        SQUARE = 1

        # ромб;
        DIAMOND = 2

        # клевер;
        CLEVER = 3

        # четырёхконечная звезда;
        FOUR_PT_STAR = 4

        # восьмиконечная звезда.
        EIGHT_PT_STAR = 5

    # перечисление "цвета фигур, которые
    # могут быть нарисованы на игровой
    # фишке".
    class ColorsOfFigures(enum.StrEnum):
        # красный.
        RED = "#E12729"

        # оранжевый.
        ORANGE = "#F37324"

        # желтый.
        YELLOW = "#F8CC1B"

        # салатовый.
        LIGHT_GREEN = "#72B043"

        # хвойный.
        CONIFERS = "#007F4E"

        # красный.
        BLUE = "#1844C7"

    def __init__(self,
                 figure: int,
                 color_of_figure: pygame.Color) -> None:
        """
        конструктор класса.
        :param figure: фигура на фишке;
        :param color_of_figure: цвет фигуры.
        """

        if figure not in [figure.value for figure in self.Figures]:
            raise ValueError("there is no such figure in the game.")
        elif not isinstance(color_of_figure, pygame.Color):
            raise ValueError("color_of_figure is not instance of pygame.Color")

        self.__figure = figure

        self.__color_of_figure = color_of_figure

    def draw_figure(self,
                    screen: pygame.Surface,
                    cell_left_corner_coordinates: tuple[int, int],
                    cell_size: int) -> None:
        """
        рисует фигуру (круг, квадрат, ромб, клевер, четырёхконечную
        звезду или восьмиконечную звезду) на фишке, которую игрок
        хочет выставить на игровое поле в определенную клетку.
        :param screen: объект окна игры;
        :param cell_left_corner_coordinates: координаты левого
        верхнего угла клетки игрового поля, в которую игрок хочет
        поместить фишку;
        :param cell_size: размер клетки;
        """

        match self.__figure:
            case self.Figures.CIRCLE:
                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + cell_size // 2,
                     cell_left_corner_coordinates[1] + cell_size // 2),
                    cell_size // 3)
            case self.Figures.SQUARE:
                rect = pygame.Rect(
                    cell_left_corner_coordinates[0] + cell_size // 6,
                    cell_left_corner_coordinates[1] + cell_size // 6,
                    2 * cell_size // 3,
                    2 * cell_size // 3)

                pygame.draw.rect(screen, self.__color_of_figure, rect, cell_size // 2)
            case self.Figures.DIAMOND:
                points = [(cell_left_corner_coordinates[0] + cell_size // 2,
                           cell_left_corner_coordinates[1] + cell_size // 6),
                          (cell_left_corner_coordinates[0] + 5 * cell_size // 6,
                           cell_left_corner_coordinates[1] + cell_size // 2),
                          (cell_left_corner_coordinates[0] + cell_size // 2,
                           cell_left_corner_coordinates[1] + 5 * cell_size // 6),
                          (cell_left_corner_coordinates[0] + cell_size // 6,
                           cell_left_corner_coordinates[1] + cell_size // 2)]

                pygame.draw.polygon(screen, self.__color_of_figure, points, 0)
            case self.Figures.CLEVER:
                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + cell_size // 2,
                     cell_left_corner_coordinates[1] + cell_size // 3),
                    cell_size // 7)

                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + cell_size // 2,
                     cell_left_corner_coordinates[1] + 2 * cell_size // 3),
                    cell_size // 7)

                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + cell_size // 3,
                     cell_left_corner_coordinates[1] + cell_size // 2),
                    cell_size // 7)

                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + 2 * cell_size // 3,
                     cell_left_corner_coordinates[1] + cell_size // 2),
                    cell_size // 7)

                pygame.draw.circle(
                    screen,
                    self.__color_of_figure,
                    (cell_left_corner_coordinates[0] + cell_size // 2,
                     cell_left_corner_coordinates[1] + cell_size // 2),
                    cell_size // 8)
            case self.Figures.FOUR_PT_STAR:
                points = [(cell_left_corner_coordinates[0] + cell_size // 6,
                           cell_left_corner_coordinates[1] + cell_size // 6),
                          (cell_left_corner_coordinates[0] + cell_size // 2,
                           cell_left_corner_coordinates[1] + cell_size // 3),
                          (cell_left_corner_coordinates[0] + 5 * cell_size // 6,
                           cell_left_corner_coordinates[1] + cell_size // 6),
                          (cell_left_corner_coordinates[0] + 2 * cell_size // 3,
                           cell_left_corner_coordinates[1] + cell_size // 2),
                          (cell_left_corner_coordinates[0] + 5 * cell_size // 6,
                           cell_left_corner_coordinates[1] + 5 * cell_size // 6),
                          (cell_left_corner_coordinates[0] + cell_size // 2,
                           cell_left_corner_coordinates[1] + 2 * cell_size // 3),
                          (cell_left_corner_coordinates[0] + cell_size // 6,
                           cell_left_corner_coordinates[1] + 5 * cell_size // 6),
                          (cell_left_corner_coordinates[0] + cell_size // 3,
                           cell_left_corner_coordinates[1] + cell_size // 2)]

                pygame.draw.polygon(screen, self.__color_of_figure, points, 0)
            case self.Figures.EIGHT_PT_STAR:
                points_1 = [(cell_left_corner_coordinates[0] + 17 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 17 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + cell_size // 2,
                             cell_left_corner_coordinates[1] + cell_size // 6),
                            (cell_left_corner_coordinates[0] + 25 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 17 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + 5 * cell_size // 6,
                             cell_left_corner_coordinates[1] + cell_size // 2),
                            (cell_left_corner_coordinates[0] + 25 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 25 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + cell_size // 2,
                             cell_left_corner_coordinates[1] + 5 * cell_size // 6),
                            (cell_left_corner_coordinates[0] + 17 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 25 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + cell_size // 6,
                             cell_left_corner_coordinates[1] + cell_size // 2)]

                pygame.draw.polygon(screen, self.__color_of_figure, points_1, 0)

                points_2 = [(cell_left_corner_coordinates[0] + 11 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 11 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + cell_size // 2,
                             cell_left_corner_coordinates[1] + 15.5 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + 31 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 11 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + 26.5 * cell_size // 42,
                             cell_left_corner_coordinates[1] + cell_size // 2),
                            (cell_left_corner_coordinates[0] + 31 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 31 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + cell_size // 2,
                             cell_left_corner_coordinates[1] + 26.5 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + 11 * cell_size // 42,
                             cell_left_corner_coordinates[1] + 31 * cell_size // 42),
                            (cell_left_corner_coordinates[0] + 15.5 * cell_size // 42,
                             cell_left_corner_coordinates[1] + cell_size // 2)]

                pygame.draw.polygon(screen, self.__color_of_figure, points_2, 0)
