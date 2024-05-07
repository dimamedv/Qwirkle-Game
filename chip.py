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

    def __init__(self, figure, color_of_figure):
        """
        конструктор класса.
        :param figure: фигура на фишке;
        :param color_of_figure: цвет фигуры.
        """

        if figure not in [figure.value for figure in self.Figures]:
            raise ValueError("there is no such figure in the game.")
        elif not isinstance(color_of_figure, pygame.Color):
            raise ValueError("color_of_figure is not instance of pygame.Color")

        self.figure = figure

        self.color_of_figure = color_of_figure

    def draw_figure(self, screen, x, y, cell_size):
        """
        рисует фигуру (круг, квадрат, ромб, клевер,
        четырёхконечную звезду или восьмиконечную
        звезду) на фишке, которую игрок хочет выставить
        на игровое поле.
        :param screen: объект окна игры;
        :param x: абсцисса верхнега угла клетки игрового
        поля, в которую игрок хочет поместить фишку;
        :param y: ордината верхнега угла клетки;
        :param cell_size: размер клетки;
        """

        match self.figure:
            case self.Figures.CIRCLE:
                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + cell_size // 2, y + cell_size // 2),
                                   cell_size // 3)
            case self.Figures.SQUARE:
                rect = pygame.Rect(x + cell_size // 6,
                                   y + cell_size // 6,
                                   2 * cell_size // 3,
                                   2 * cell_size // 3)

                pygame.draw.rect(screen, self.color_of_figure, rect, cell_size // 2)
            case self.Figures.DIAMOND:
                points = [(x + cell_size // 2, y + cell_size // 6),
                          (x + 5 * cell_size // 6, y + cell_size // 2),
                          (x + cell_size // 2, y + 5 * cell_size // 6),
                          (x + cell_size // 6, y + cell_size // 2)]

                pygame.draw.polygon(screen, self.color_of_figure, points, 0)
            case self.Figures.CLEVER:
                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + cell_size // 2, y + cell_size // 3),
                                   cell_size // 7)

                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + cell_size // 2, y + 2 * cell_size // 3),
                                   cell_size // 7)

                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + cell_size // 3, y + cell_size // 2),
                                   cell_size // 7)

                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + 2 * cell_size // 3, y + cell_size // 2),
                                   cell_size // 7)

                pygame.draw.circle(screen,
                                   self.color_of_figure,
                                   (x + cell_size // 2, y + cell_size // 2),
                                   cell_size // 8)
            case self.Figures.FOUR_PT_STAR:
                points = [(x + cell_size // 6, y + cell_size // 6),
                          (x + cell_size // 2, y + cell_size // 3),
                          (x + 5 * cell_size // 6, y + cell_size // 6),
                          (x + 2 * cell_size // 3, y + cell_size // 2),
                          (x + 5 * cell_size // 6, y + 5 * cell_size // 6),
                          (x + cell_size // 2, y + 2 * cell_size // 3),
                          (x + cell_size // 6, y + 5 * cell_size // 6),
                          (x + cell_size // 3, y + cell_size // 2)]

                pygame.draw.polygon(screen, self.color_of_figure, points, 0)
            case self.Figures.EIGHT_PT_STAR:
                points_1 = [(x + 17 * cell_size // 42, y + 17 * cell_size // 42),
                            (x + cell_size // 2, y + cell_size // 6),
                            (x + 25 * cell_size // 42, y + 17 * cell_size // 42),
                            (x + 5 * cell_size // 6, y + cell_size // 2),
                            (x + 25 * cell_size // 42, y + 25 * cell_size // 42),
                            (x + cell_size // 2, y + 5 * cell_size // 6),
                            (x + 17 * cell_size // 42, y + 25 * cell_size // 42),
                            (x + cell_size // 6, y + cell_size // 2)]

                pygame.draw.polygon(screen, self.color_of_figure, points_1, 0)

                points_2 = [(x + 11 * cell_size // 42, y + 11 * cell_size // 42),
                            (x + cell_size // 2, y + 15.5 * cell_size // 42),
                            (x + 31 * cell_size // 42, y + 11 * cell_size // 42),
                            (x + 26.5 * cell_size // 42, y + cell_size // 2),
                            (x + 31 * cell_size // 42, y + 31 * cell_size // 42),
                            (x + cell_size // 2, y + 26.5 * cell_size // 42),
                            (x + 11 * cell_size // 42, y + 31 * cell_size // 42),
                            (x + 15.5 * cell_size // 42, y + cell_size // 2)]

                pygame.draw.polygon(screen, self.color_of_figure, points_2, 0)
