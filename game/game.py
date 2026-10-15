"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Управление монетами, инвентарём и действиями питомца."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создать игру без монет и покупок, ничего не возвращая.

        :param tamagochi: питомец
        :param clicker: источник заработка
        :param all_food: каталог еды
        :param all_medicine: каталог лекарств
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = 0

    def _choose_item(self, items: list[Food] | list[Medicine]) -> int | None:
        """Вернуть индекс выбранного предмета или None при отмене.

        :param items: каталог или инвентарь для выбора
        """
        if not items:
            print('Список пуст.')
            return None
        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')
        print('0. Отмена')
        while True:
            try:
                number = int(input('Выберите предмет: '))
            except ValueError:
                print('Введите номер предмета.')
                continue
            if number == 0:
                return None
            if 1 <= number <= len(items):
                return number - 1
            print('Нет предмета с таким номером.')

    def work(self) -> int:
        """Заработать монеты и вернуть доход за один ход.

        :raises TamagochiIsGone: если питомец умер после хода
        """
        self.clicker.click()
        income = self.clicker.income_per_click
        self._coins += income
        self.tamagochi.update()
        return income

    def buy_food(self) -> None:
        """Купить выбранную еду и завершить ход, ничего не возвращая.

        :raises NotEnoughMoney: если монет недостаточно
        :raises TamagochiIsGone: если питомец умер после хода
        """
        index = self._choose_item(self._all_food)
        if index is None:
            return
        food = self._all_food[index]
        if self._coins < food.price:
            raise NotEnoughMoney('Не хватает монет на еду.')
        self._coins -= food.price
        self._food.append(food)
        self.tamagochi.update()

    def buy_medicine(self) -> None:
        """Купить новое лекарство и завершить ход, ничего не возвращая.

        :raises NotEnoughMoney: если монет недостаточно
        :raises TamagochiIsGone: если питомец умер после хода
        """
        index = self._choose_item(self._all_medicine)
        if index is None:
            return
        medicine = self._all_medicine[index]
        if self._coins < medicine.price:
            raise NotEnoughMoney('Не хватает монет на лекарство.')
        self._coins -= medicine.price
        self._medicine.append(replace(medicine, uses=0))
        self.tamagochi.update()

    def feed_tamagochi(self) -> None:
        """Скормить выбранную еду и завершить ход, ничего не возвращая.

        :raises TamagochiIsGone: если питомец умер после хода
        """
        index = self._choose_item(self._food)
        if index is None:
            return
        self.tamagochi.feed(self._food[index])
        self._food.pop(index)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Применить выбранное лекарство и завершить ход; вернуть None.

        :raises TamagochiIsGone: если питомец умер после хода
        """
        index = self._choose_item(self._medicine)
        if index is None:
            return
        medicine = self._medicine[index]
        if medicine.is_empty():
            print('Лекарство закончилось.')
            return
        self.tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine.pop(index)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть и завершить ход; вернуть None.

        :raises TamagochiIsGone: если питомец умер после хода
        """
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем и завершить ход; вернуть None.

        :raises TamagochiIsGone: если питомец умер после хода
        """
        self.tamagochi.play()
        self.tamagochi.update()

    def get_status(self) -> dict[str, int]:
        """Вернуть показатели питомца и текущее число монет."""
        status = self.tamagochi.status.copy()
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        """Вернуть список купленной еды."""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Вернуть список купленных лекарств."""
        return self._medicine
