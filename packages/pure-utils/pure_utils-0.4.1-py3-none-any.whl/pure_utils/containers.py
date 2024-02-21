"""Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.)."""

from typing import Any, Generator, Mapping, Optional, Sequence, TypeVar

T = TypeVar("T")


def bisect(source_list: list) -> tuple[list, list]:
    """Разделить список на две части/половины по количеству элементов.

    Функция не изменяет исходный список.

    Args:
        source_list: Исходный список.

    Returns:
        Двухэлементный кортеж, содержащий два списка:
        первый список представляет собой первую половину исходного списка,
        а второй список в кортеже - вторую половину исходного списка соответственно.

    Raises:
        AssertionError: Сработает, если передан пустой исходный список.
    """
    assert source_list
    length = len(source_list)
    return (source_list[: length // 2], source_list[length // 2 :])


def first(collection: Sequence[T]) -> Optional[T]:
    """Получить значение первого элемента из гомогенной коллекции.

    Args:
        collection: Коллекция гомогенных элементов.

    Returns:
        Значение первого элемента коллекции, либо None в случае отсутствия такового.

    Пример использования:

    .. code-block:: python

        from utils.common import first

        seq = (1, 2, 3)
        print(first(seq))  # 1

        seq = []
        print(first(seq))  # None
    """
    return next((_ for _ in collection), None)


def flatten(source_seequence: list | tuple | set) -> Generator[Any, None, None]:
    """Сделать итерируемую последовательность "плоской".

    Плоская последовательность - такая последовательность,
    элементы которой находятся на первом уровне вложенности (одномерный массив).

    Функция не изменяет исходную последовательность и может работать с типами: list, tuple, set.

    Args:
        source_seequence: Исходная последовательность для "уплощения".

    Returns:
        Возвращает генератор функции "уплощения".

    Пример использования:

    .. code-block:: python

        seq = [[1], [2], [3], [4], [5]]
        result = list(flatten(seq))
        print(result)  # [1, 2, 3, 4, 5]

        seq = [[[[[[1]]]]], [[[[[2]]]]], [[[[[3]]]]], [[[[[4]]]]], [[[[[5]]]]]]
        result = list(flatten(seq))
        print(result)  # [1, 2, 3, 4, 5]
    """
    if isinstance(source_seequence, (list, tuple, set)):
        for _ in source_seequence:
            yield from flatten(_)
    else:
        yield source_seequence


def get_or_else(sequence: Sequence[T], index: int, default: Optional[T] = None) -> Optional[T]:
    """Получить значение элемента, или, в случае его отсутствия, значение по умолчанию.

    Используется для безопасного получения значения элемента последовательности.

    Args:
        sequence: Гомогенная последовательность элементов.
        index: Индекс, по которому требуется получить значение элемента.
        default: Опциональное значение по умолчанию, которое будет возвращено
                 в случае отсутствия элемента по указанному индексу.

    Returns:
        Значение элемента последовательности по указанному индексу,
        или же значение по умолчанию, если элемента по указанному индексу не найдено.

    Пример использования:

    .. code-block:: python

        from utils.common import get_or_else

        seq = (1, 2, 3)
        print(get_or_else(seq, 0))  # 1
        print(get_or_else(seq, 3))  # None
        print(get_or_else(seq, 3, -1))  # -1

        seq = ["a", "b", "c"]
        print(get_or_else(seq, 3, "does not exists"))  # does not exists
    """
    try:
        return sequence[index]
    except IndexError:
        return default


def omit(source_dict: dict, keys_to_omit: list[str]) -> dict:
    """Удалить пары ключ-значение из исходного словаря по списку ключей в keys_to_omit.

    Работает с копией словаря (исходный словарь не изменяется).

    Args:
        source_dict: Исходный словарь с данными.
        keys_to_omit: Список ключей, по которым требуется опустить данные в исходном словаре.

    Returns:
        Словарь с опущенными данными на основании списка ключей.

    Пример использования:

    .. code-block:: python

        source_dict = {"key1": "val1", "key2": "val2", "key3": "val3", "key4": "val4"}
        result = omit(source_dict, ["key2", "key4"] )
        print(result)  # {"key1": "val1", "key3": "val3"}
    """
    keys_diff = symmdiff(list(source_dict.keys()), keys_to_omit)
    return {key: source_dict[key] for key in keys_diff if key in source_dict}


def paginate(source_list: list, limit: int) -> list[list]:
    """Разбить исходный список на страницу(ы), согласно указанному размеру/пределу.

    Функция не изменяет исходный список.

    Args:
        source_list: Исходный список.
        limit: Предел количества элементов в списке-странице.

    Returns:
        Список, содержащий "страницу" - отсеченный кусок элементов исходного списка.

    Raises:
        AssertionError: Сработает, если передан пустой исходный список,
                        либо же если передан отрицательный предел.
    """
    assert source_list
    assert limit > 0
    lenght = len(source_list)
    return [source_list[start : start + limit] for start in range(0, lenght, limit)]


def pick(source_dict: dict, allowed_keys: list[str]) -> dict:
    """Выбрать из исходного словаря пары ключ-значения, согласно указанному в списке allowed_keys.

    Все остальные значения словаря будут опущены.
    Функция работает с копией словаря (исходный словарь не изменяется).

    Args:
        source_dict: Исходный словарь с данными.
        allowed_keys: Список ключей, по которым требуется выбрать данные из исходного словаря.

    Returns:
        Словарь с выбранными данными на основании списка ключей

    Пример использования:

    .. code-block:: python

         source_dict = {"key1": "val1", "key2": "val2", "key3": "val3"}
         result = pick(source_dict, ["key2", "key3"])
         print(result)  # {"key1": "val1"}
    """
    return {key: source_dict[key] for key in allowed_keys if key in source_dict}


def symmdiff(l1: list, l2: list) -> list:
    """Получить симметрическую разность элементов двух списков.

    Args:
        l1: Первый список значений, для образования множества СЛЕВА.
        l2: Второй список значений, для образования множества СПРАВА.

    Returns:
        Симметрическую разность элементов двух списков (двух множеств на основании исходных список).

    Пример использования:

    .. code-block:: python

         l1 = [ 'a', 'b', 'c' ]
         l2 = [ 'e', 'b', 'a' ]
         result = symmdiff( l1, l2 )
         print(result)  # ['c', 'e']
    """
    return list(set(l1).symmetric_difference(set(l2)))


def unpack(obj: Mapping, attributes: Sequence[str]) -> tuple:
    """Распаковать значения итерируемого объекта в отдельные переменные.

    Args:
        obj: Итерируемый объект.
        attributes: Список названий аттрибутов, значения которых нужно распаковать.

    Returns:
        Кортеж распакованных значений, указанных аттрибутов.

    Пример использования:

    .. code-block:: python

        from utils.common import unpack

        d = {"a": 1, "b": True, "c": {"d": "test"}}
        print(unpack(d, ("a", "b")))  # (1, True)

        d = {"a": 1, "b": True, "c": {"d": "test"}}
        print(unpack(d, ("e", "f")))  # (None, None)

        class A:
            def __init__(self):
                self.a = 100
                self.b = 500

        obj = A()
        unpack(obj, ("a", "b", "c"))  # (100, 500, None)
    """
    if isinstance(obj, dict):
        return tuple(obj.get(attr) for attr in attributes)

    unpacked_values = []

    for attr in attributes:
        try:
            unpacked_values.append(getattr(obj, attr))
        except AttributeError:
            unpacked_values.append(None)

    return tuple(unpacked_values)
