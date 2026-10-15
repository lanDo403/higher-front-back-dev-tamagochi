"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом в заданном диапазоне."""

    def __init__(self, min_income: int = 10, max_income: int = 20) -> None:
        """Создать кликер, ничего не возвращая.

        :param min_income: минимальный доход за клик
        :param max_income: максимальный доход за клик
        :raises ValueError: если диапазон не задаёт положительный доход
        """
        if min_income <= 0 or max_income < min_income:
            raise ValueError('Нужен положительный диапазон дохода')
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        """Рассчитать доход нового клика, ничего не возвращая."""
        self._income_per_click = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        """Вернуть доход последнего клика, до первого клика — ноль."""
        return self._income_per_click
