from decimal import Decimal


class Account:
    """
    Cуперкласс для банковского счета.

    Parameters
    ----------
    self.__account_number : str
        Номер банковского счёта.

    self.__user_name : str
        Наименование пользователя.

    self.__balance : Decimal
        Баланс банковского счёта.
    """

    def __init__(self, account_number: str, user_name: str, balance: Decimal):
        """ Конструктор класса. """
        self.__account_number = account_number
        self.__user_name = user_name
        self.__balance = balance

        # Установка лимитов по счетам.
        self.__min_limit = 0  # Минимальный лимит.
        self.__max_limit = 10000  # Максимальный лимит.

        # Процентная ставка начисления в месяц для счетов (по умолчанию 0%).
        self.__interest = 0 / 12

    def get_account_number(self):
        """ Получить номер счёта. """
        return self.__account_number

    def get_customer_name(self) -> str:
        """ Получить имя клиента. """
        return self.__user_name

    def get_balance(self) -> Decimal:
        """ Получить баланс. """
        return self.__balance

    def set_balance(self, new_balance: Decimal) -> bool:
        """
        Установить баланс.

        Parameters
        ----------
        new_balance : Decimal
            Новый баланс для счёта.

        Returns
        -------

        bool
            Баланс установлен.
        """
        self.__balance = new_balance.quantize(Decimal("1.00"))
        return True

    def check_limit(self, new_amount: Decimal) -> bool:
        """ Проверка лимитов. """

        # Новая сумма больше, чем максимальный лимит по счёту.
        if new_amount > self.__max_limit:
            return False

        # Новая сумма меньше, чем минимальный лимит по счёту.
        if new_amount < self.__min_limit:
            return False

        # Все проверки пройдены.
        return True

    def deposit(self, amount: Decimal) -> bool:
        """
        Внести деньги на счёт.

        Parameters
        ----------

        amount : Decimal
            Сумма пополнения.

        Returns
        -------

        bool
            Успешность вноса денег на счёт.
        """

        # Высчитываем предположительный баланс.
        new_balance = self.__balance + amount
        # Проверяем лимит.
        if self.check_limit(new_balance):
            # Устанавливаем баланс и возвращаем результат успешности установки.
            return self.set_balance(new_balance)
        else:
            return False

    def withdraw(self, amount: Decimal) -> bool:
        """
        Снять деньги со счёта.

        Parameters
        ----------

        amount : Decimal
            Сумма снятия.

        Returns
        -------
        bool
            Успешность снятия денег со счёта.
        """
        # Высчитываем предположительный баланс.
        new_balance = self.__balance - amount
        # Проверяем лимит.
        if self.check_limit(new_balance):
            # Устанавливаем баланс и возвращаем результат успешности установки.
            return self.set_balance(new_balance)
        else:
            return False

    def display(self) -> None:
        """ Вывод информации по счету. """
        print("Номер счета:", self.__account_number)
        print("Клиент:", self.__user_name)
        print(f"Баланс (λ): {self.__balance}")

    def display_monthly_statement(self) -> None:
        """ Вывод месячного отчёта. """
        print(f'Ежемесячный отчет по {self.get_account_title()} ')
        self.display()

    def get_account_type(self) -> str:
        """ Получить тип счёта. """
        return self.__class__.__name__[0]  # Тип счёта по первой букве класса.

    def get_account_title(self) -> str:
        """ Получить название счёта. """
        match self.get_account_type():
            case 'C':
                return 'текущему счету'
            case 'S':
                return 'сберегательному счёту'
        return 'unknown'
