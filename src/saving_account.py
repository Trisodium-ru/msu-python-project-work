from decimal import Decimal

from src.account import Account


class SavingAccount(Account):  # Наследование суперкласса.
    """ Сберегательный счёт клиента. """

    def __init__(self, account_number: str, user_name: str, balance: Decimal):
        """ Конструктор класса. """
        super().__init__(account_number, user_name, balance)
        # Для сберегательного счёта указываем ежемесячную ставку в процентах.
        self.__interest = 0.01 / 12

    def display_monthly_statement(self) -> None:
        """ Переопределение вывода ежемесячной выписки по счёту. """

        # Устанавливаем накопленные проценты за месяц.
        self.set_balance(self.get_balance() * Decimal(1 + self.__interest))
        # Выводим отчёт.
        print("Ежемесячная выписка по сберегательному счету ")
        self.display()
