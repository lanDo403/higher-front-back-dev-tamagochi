from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """Запустить консольную игру до смерти питомца или выхода; вернуть None."""
    print("Добро пожаловать в Тамагочи-кликер!")
    try:
        name = input('Введите имя питомца: ').strip()
        while not name:
            print('Имя не должно быть пустым.')
            name = input('Введите имя питомца: ').strip()
    except (EOFError, KeyboardInterrupt):
        print('\nИгра завершена.')
        return

    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print(f'Ваш питомец: {name}.')
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\n{name}: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print(f"======={name} болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        output = ''
        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case "2":
                    game.buy_food()
                case "3":
                    game.buy_medicine()
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = f'Вы поиграли с питомцем по имени {name}'
                case "7":
                    game.rest_tamagochi()
                    output = f'{name} отдохнул'
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except NotEnoughMoney as error:
            output = str(error)
        except TamagochiIsGone as error:
            print(f'{name}: {error}')
            break
        except (EOFError, KeyboardInterrupt):
            print('\nИгра завершена.')
            break


if __name__ == "__main__":
    main()
