import datetime
from decimal import Decimal


class Transaction:

    def __init__(self, transaction_date: str, account_type: str, account_number: str, transaction_type: str, transaction_amount: Decimal):
        """
        Одна транзакция: содержит данные по транзакции.

        Parameters
        ----------
        self.__transaction_date : datetime.date
            Дата транзакции.

        self.__account_type : str
            Тип счёта (S - сберегательный, C - депозитный).

        self.__account_number : str
            Номер счёта.

        self.__transaction_type : str
            Тип операции (W - снятие, D - пополнение).

        self.__amount : Decimal
            Сумма операции.
        """

        # Инициализация атрибутов класса.
        self.__transaction_date = datetime.date(*[int(i) for i in transaction_date.split('-')])
        self.__account_type = account_type
        self.__account_number = account_number
        self.__transaction_type = transaction_type
        self.__transaction_amount = transaction_amount

    def get_transaction_date(self) -> datetime.date:
        """ Получить дату транзакции. """
        return self.__transaction_date

    def get_account_number(self) -> str:
        """ Получить номер счёта транзакции. """
        return self.__account_number

    def get_transaction_type(self) -> str:
        """ Получить тип транзакции. """
        return self.__transaction_type

    def get_transaction_amount(self) -> Decimal:
        """ Получить сумму транзакции. """
        return self.__transaction_amount
