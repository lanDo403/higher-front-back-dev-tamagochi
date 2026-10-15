"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Питомец с голодом, усталостью, здоровьем, энергией и болезнью."""

    def __init__(self) -> None:
        """Создать здорового отдохнувшего питомца, ничего не возвращая."""
        self._hunger = 0
        self._tiredness = 0
        self._hp = 100
        self._energy = 100
        self._sick = False

    def feed(self, food: Food) -> None:
        """Уменьшить голод, ничего не возвращая.

        :param food: еда с указанным насыщением
        """
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """Потратить энергию, повысить голод и усталость; вернуть None."""
        self._energy = max(0, self._energy - 10)
        self._hunger = min(100, self._hunger + 10)
        self._tiredness = min(100, self._tiredness + 10)

    def rest(self) -> None:
        """Восстановить силы, слабее при болезни; ничего не возвращать."""
        recovery = 10 if self.is_sick() else 20
        self._energy = min(100, self._energy + recovery)
        self._tiredness = max(0, self._tiredness - recovery)

    def heal(self, medicine: Medicine) -> None:
        """Применить неизрасходованное лекарство, ничего не возвращая.

        :param medicine: лекарство, счётчик использований которого вырастет
        """
        if medicine.is_empty():
            return
        self._hp = min(100, self._hp + medicine.heal_hp)
        self._sick = False
        medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        """Вернуть новый словарь с числовыми показателями питомца."""
        return {
            'hunger': self._hunger,
            'tiredness': self._tiredness,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """Вернуть True, пока здоровье не опустилось ниже нуля."""
        return self._hp >= 0

    def is_sick(self) -> bool:
        """Вернуть True, если питомец болен."""
        return self._sick

    def update(self) -> None:
        """Изменить показатели за ход, ничего не возвращая.

        :raises TamagochiIsGone: если здоровье питомца ниже нуля
        """
        if not self.is_alive():
            raise TamagochiIsGone('Питомец умер. Игра окончена.')
        self._hunger = min(100, self._hunger + 2)
        self._tiredness = min(100, self._tiredness + 2)
        self._energy = max(0, self._energy - 2)
        if self._hunger >= 70 or self._tiredness >= 70:
            self._sick = True
        if self._hunger == 100 or self._energy == 0:
            self._hp -= 10
        if self.is_sick():
            self._hp -= 5
            self._tiredness = min(100, self._tiredness + 5)
        if not self.is_alive():
            raise TamagochiIsGone('Питомец умер. Игра окончена.')
