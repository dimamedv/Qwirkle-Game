import inspect


def get_arg_name(arg) -> str:
    """
    возвращает имя аргумента, переданного
    в вызове функции.
    :param arg: аргумент.
    :return: имя аргумента, переданного
    в вызове функции.
    """

    frame = inspect.currentframe().f_back

    arg_name = [name for name, val in frame.f_locals.items() if val is arg]

    return arg_name[0] if arg_name else "unknown"


def pass_first_arg_name(function):
    """
    декоратор, автоматически передающий
    в функцию имя переменной, переданной
    в качестве первого аргумента, в качестве
    другого аргумента.
    :param function: декорируемая функция.
    """

    def wrapper(*args, **kwargs):
        kwargs["first_arg_name"] = get_arg_name(args[0])

        return function(*args, **kwargs)

    return wrapper


def pass_second_arg_name(function):
    """
    декоратор, автоматически передающий
    в функцию имя переменной, переданной
    в качестве второго аргумента, в качестве
    другого аргумента.
    :param function: декорируемая функция.
    """

    def wrapper(*args, **kwargs):
        kwargs["first_arg_name"] = get_arg_name(args[1])

        return function(*args, **kwargs)

    return wrapper


@pass_first_arg_name
def validate_int_value(
        value: int,
        valid_value_borders: tuple[[int, None], [int, None]],
        first_arg_name: str = "unknown") -> None:
    """
    производит валидацию целочисленного значения.
    :param value: значение;
    :param valid_value_borders: границы валидного
    значения;
    :param first_arg_name: имя переменной.
    """

    object_name = first_arg_name

    if valid_value_borders[0] is None:
        invalid_value_condition = value > valid_value_borders[1]
    elif valid_value_borders[1] is None:
        invalid_value_condition = value < valid_value_borders[0]
    else:
        invalid_value_condition = (value < valid_value_borders[0] or
                                   value > valid_value_borders[1])

    if invalid_value_condition:
        raise ValueError(f"invalid value of {object_name}.")


@pass_first_arg_name
def validate_object_type(
        validated_object: object,
        required_type_of_object: object,
        first_arg_name: str = "unknown") -> None:
    """
    производит валидацию типа объекта.
    :param validated_object: валидируемый объект;
    :param required_type_of_object: требуемый
    тип объекта;
    :param first_arg_name: имя переменной.
    """

    object_name = first_arg_name

    if not isinstance(validated_object, required_type_of_object):
        raise ValueError(f"{object_name} must be object of "
                         f"{required_type_of_object}.")


@pass_first_arg_name
def validate_container_elements_type(
        validated_container: list | object,
        required_type_of_element: object,
        first_arg_name: str = "unknown") -> None:
    """
    производит валидацию типа элементов контейнера.
    :param validated_container: валидируемый контейнер;
    :param required_type_of_element: требуемый
    тип элемента списка;
    :param first_arg_name: имя списка.
    """

    container_name = first_arg_name

    if not all(isinstance(item, required_type_of_element)
               for item in validated_container):
        raise TypeError(f"not all elements of {container_name} are objects of "
                        f"{required_type_of_element}.")


@pass_first_arg_name
@pass_second_arg_name
def validate_equality(
        first_validated_object: object,
        second_validated_object: object,
        first_arg_name: str = "unknown",
        second_arg_name: str = "unknown") -> None:
    """
    производит валидацию равенства двух объектов.
    :param first_validated_object: первый валидируемый
    объект;
    :param second_validated_object: второй валидируемый
    объект;
    :param first_arg_name: имя первого объекта;
    :param second_arg_name: имя второго объекта.
    """

    first_object_name = first_arg_name
    second_object_name = second_arg_name

    if first_validated_object != second_validated_object:
        raise ValueError(f"{first_object_name} are not equal to "
                         f"{second_object_name}.")


@pass_second_arg_name
@pass_second_arg_name
def validate_presence_in_container(
        validated_object: object,
        container: object,
        first_arg_name: str = "unknown",
        second_arg_name: str = "unknown") -> None:
    """
    производит валидацию нахождения объекта в контейнере.
    :param validated_object: валидируемый объект;
    :param container: контейнер;
    :param first_arg_name: имя объекта;
    :param second_arg_name: имя контейнера.
    """

    object_name = first_arg_name
    container_name = second_arg_name

    if validated_object not in container:
        raise ValueError(f"{object_name} is not in "
                         f"{container_name}.")
