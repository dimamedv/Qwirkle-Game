from validators import *


# класс "игрок".
class Player:
    def __init__(self, nickname: str) -> None:
        """
        конструктор класса.
        :param nickname: никнейм игрока.
        """

        validate_object_type(nickname, str)

        self.__nickname = nickname

    @property
    def nickname(self) -> str:
        """
        возвращает значение поля __nickname.
        :return: значение поля __nickname.
        """

        return self.__nickname

    @nickname.setter
    def nickname(self, new_nickname: str) -> None:
        """
        устанавливает новое значение поля __nickname.
        :param new_nickname: новое значение поля
        __nickname.
        """

        validate_object_type(new_nickname, str)

        self.__nickname = new_nickname
