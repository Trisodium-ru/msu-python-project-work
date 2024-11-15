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

    Returns
    -------
    int
        Сум
    """

    __account_number = ''

    def __init__(self, account_number: str, user_name: str, balance: Decimal):
        """ Конструктор класса. """
        self.__account_number = account_number
        self.__customer_name = user_name
        self.__balance = balance

        # Процентная ставка начисления для счетов (по умолчанию 0%).
        self.__interest = 0.01 / 12

    def getAccountNo(self):
        ''' получить номер счета '''
        return self.__AccountNo

    def getCustomerName(self):
        ''' получить имя клиента '''
        return self.__CustomerName

    def getBalance(self):
        ''' получить баланс '''
        return self.__Balance

    def setBalance(self, newBalance):
        ''' установить баланс '''
        self.__Balance = newBalance

    def deposit(self, amount):
        ''' внести депозит '''
        self.__Balance = self.__Balance + amount

    def withdraw(self, amount):
        ''' снять деньги '''
        self.__Balance = self.__Balance - amount

    def display(self):
        ''' информация по счету '''
        print("Номер счета:", self.__AccountNo)
        print("Клиент:", self.__CustomerName)
        print("Баланс: ${0:.2f}".format(self.__Balance))

    # __class__.__name__
    def display_monthly_statement(self):
        print(f'Ежемесячный отчет по {self.get_account_title()} ')
        self.display()

    def get_account_title(self):
        match self.__class__.__name__:
            case 'SavingAccount':
                return 'текущему счету'
            case 'SavingAccount':
                return 'сберегательному счёту'
        return 'unknown'

