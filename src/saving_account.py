from decimal import Decimal

from src.account import Account


class SavingAccount(Account):  # Наследование суперкласса.
    """ Сберегательный счёт клиента. """

    def __init__(self, account_number: str, user_name: str, balance: Decimal):
        """ Конструктор класса. """
        super().__init__(account_number, user_name, balance)
        # Для сберегательного счёта указываем ежемесячную ставку в процентах.
        self.__interest = 0.01 / 12

    def display_monthly_statement(self):
        self.setBalance(self.getBalance() * (1 + self.__interest))
        print("Ежемесячная выписка по сберегательному счету ")
        super().display()
