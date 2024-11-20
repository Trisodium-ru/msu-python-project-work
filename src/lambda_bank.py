import random, datetime
from decimal import Decimal
from time import sleep

from account import Account
from src import reader
from transcation import Transaction


class LambdaBank:
    """ Основной класс для запуска приложения. """

    def __init__(self, logging: bool = False, logging_pause: int = 0):
        """
        Инициализация приложения LambdaBank.

        Parameters
        ----------
        logging : bool = True
            Ведение логов основного потока приложения.

        logging_pause : int = 1
            Пауза после логирования приложения. Только эстетический эффект.

        """

        # Настройки приложения.
        self.__title = 'λambda Bank'  # Название приложения.

        # Возможные типы банковских счетов.
        self.__account_types = (
            'S',  # Сберегательный счёт.
            "C",  # Текущий счёт.
        )

        # Возможные типы транзакций.
        self.__transactions_types = (
            'W',  # Снятие (расходная операция).
            "D",  # Пополнение (доходная операция).
        )

        # Пути для файлов данных (для сессии программы создаются свои файлы из оригинальных).
        self.__original_accounts_file_path = 'database/original/accounts.csv'  # Оригинальный файл данных счетов.
        self.__original_transactions_file_path = 'database/original/transactions.csv'  # Оригинальный файл данных транзакций.
        self.__session_accounts_file_path = 'database/session/accounts.csv'  # База данных счетов сессии приложения.
        self.__session_transactions_file_path = 'database/session/transactions.csv'  # Оригинальный файл данных транзакций.

        # Настройки логирования (опционально).
        self.__logging = logging # Включить логирование.
        self.__logging_pause = logging_pause # Пауза между выводом.

        # Существующие аттрибуты класса.
        self.__accounts = None # Список счетов CurrencyAccount | SavingAccount.
        self.__accounts_numbers = None  # Уникальный список номеров счетов пользователей.
        self.__users_names = None  # Уникальный список ФИО пользователей.
        self.__transactions = []  # Список транзакий ожидающих обработки.
        self.__completed_transactions = []  # Список обработанных транзакий.

    def start(self):
        self.log(f'! Старт приложения "{self.__title}".')
        self.prepare_session_files()

    def prepare_session_files(self):
        """
        Процедура подготовки файлов сессии для работы.
        Копирует изначальные файлы `original` в `session` для работы с ними.
        Исходные и конечные файлы задаются при инициализации __init__.
        """

        # Копирование файла счетов.
        self.log(f'↻ Файл счетов копируется.')
        reader.copy_file(self.__original_accounts_file_path, self.__session_accounts_file_path)

        # Копирование файла транзакций.
        self.log(f'↻ Файл транзакий копируется.')
        reader.copy_file(self.__original_transactions_file_path, self.__session_transactions_file_path)

        self.log(f'! Все файлы успешно подготовлены.')

    def add_transaction(self, transaction: Transaction):
        """ Добавяление транзакции в список транзакций к обработке. """
        self.__transactions.append(transaction)

    def carry_out_transactions(self):
        """
        Проводка транзакций в списке ожидания проводки.

        Returns
        -------
        int
            Количество проведённых транзакций.
        """

        # Количество проведённых транзакций.
        number_of_carry_out_transactions = 0

        # Перебираем список транзакий в ожидании.
        while len(self.__transactions) > 0:
            # Берём самую первую транзакцию.
            current_transaction = self.__transactions.pop(0)

            # Проводка транзакции.
            if self.carry_out_transaction(current_transaction):
                # Проведённую транзакцию переносим в список завершённых.
                self.__completed_transactions.append(current_transaction)

                # Запись количества проведённых транзакций.
                number_of_carry_out_transactions += 1

        # Возврат количества проведённых транзакций.
        return number_of_carry_out_transactions

    def get_account(self, account_number: str) -> Account | None:
        """
        Поиск счёта по номеру счёта.

        Parameters
        ----------

        account_number : str
            Номер счёта.

        Returns
        -------
        CurrentAccount | SavingAccount | None
            Счёт пользователя, если найден.
        """

        # Поиск по номеру счёта в списке счетов.
        for account in self.__accounts:
            if account.get_account_number() == account_number:
                return account

        # Счёт не найден.
        return None

    def carry_out_transaction(self, transaction: Transaction):
        """
        Проводка одной транзакции.

        Returns
        -------
        bool
            Успешность проводки транзакции.
        """

        # Проверка транзакции на существование типа.
        transaction_type = transaction.get_transaction_type()
        if transaction_type not in self.__transactions_types:
            self.log(f'Ошибка проводки транзакции 1: тип транзакции {transaction_type} не найден.')
            return False

        # Поиск аккаунта пользователя из транзакции.
        account = self.get_account(transaction.get_account_number())
        if not account:
            self.log(f'Ошибка проводки транзакции 2: счёт транзакции {account} не найден.')
            return False

        # Списание или пополнение в зависимости от типа.
        if transaction_type == 'D':  # Пополнение.
            if not account.deposit(transaction.get_transaction_amount()):
                self.log(f'Ошибка проводки транзакции 3: нельзя произвести пополнение {transaction.get_transaction_amount()} (лимиты счёта).')
                return False
        elif transaction_type == 'W':  # Снятие.
            if not account.withdraw(transaction.get_transaction_amount()):
                self.log(f'Ошибка проводки транзакции 4: нельзя произвести снятие {transaction.get_transaction_amount()} (лимиты счёта).')
                return False

        # Успешная проводка транзакции.
        return True

    def carry_out_transactions_from_file(self):
        """
        Проводка транзакций из файла сессии.
        """

        # Получаем список счетов.
        self.log('↻ Формирование списка счетов из файла.')
        self.__accounts, self.__accounts_numbers, self.__users_names = reader.read_accounts(
            self.__session_accounts_file_path)
        self.log(
            f'! В файле счетов найдено {len(self.__accounts)} строк, номеров счетов: {len(self.__accounts_numbers)}, ФИО: {len(self.__users_names)}.')

        # Получаем список транзакций.
        self.log('↻ Формирование списка транзакций из файла.')
        self.__transactions = reader.read_transactions(self.__session_transactions_file_path)
        self.log(f'! В файле транзакций найдено {len(self.__transactions)} транзакций.')

        # Проводим все транзакции по счетам.
        self.log('↻ Проводка транзакций по счетам пользователей.')
        number_carry_out = self.carry_out_transactions()
        self.log(f'! Транзакции из файла успешно проведены: {number_carry_out}шт.')

    def generate_files_records(self, from_number_recodrs: int, to_number_records: int):
        """ Генерация данных: счетов и транзакций. """

        # Создаём словарь для генерации с весом.
        letters = {
            'q': 10, 'w': 10, 'e': 90, 'r': 30, 't': 20, 'y': 90, 'u': 90, 'i': 90, 'o': 90, 'p': 20,
            'a': 90, 's': 20, 'd': 40, 'f': 30, 'g': 20, 'h': 50, 'j': 30, 'k': 30, 'l': 20, 'z': 10,
            'x': 10, 'c': 50, 'v': 30, 'b': 80, 'n': 80, 'm': 70,
        }
        # Получаем списки для генерации.
        letter_keys = list(letters.keys())  # Список букв.
        letter_values = list(letters.values())  # Список веса для генератора.

        # Формируем случайные имена (3 слова по 2-5 букв).
        random_names = []
        for _ in range(10):
            random_names.append(' '.join(
                [''.join(random.choices(letter_keys, weights=letter_values, k=random.randint(2, 5))) for _ in
                 range(3)]).title())

        ''' Генерация счетов и клиентов. '''
        # Создаём и записываем случайные данные в файл построчно.
        last_account_number = 10
        accounts = []
        # Открываем файл для чтения в режими дозаписи.
        accounts_file = open(self.__session_accounts_file_path, 'a')
        for _ in range(random.randint(from_number_recodrs, to_number_records)):
            # Берём случайное имя из сгенерированных.
            name = random.choice(random_names)

            # Берём случайный тип счёта из возможных.
            account_type = random.choice(self.__account_types)

            # Генерируем новый номер счёта.
            last_account_number += random.randint(1, 10)
            account_number = f'00000{last_account_number}'[-5:]

            # Генерируем баланс (рубли и копейки).
            rub = random.randint(800, 5_000)
            kop = random.randint(0, 99)

            # Запись строки в файл.
            accounts_file.write(f'{account_type},{account_number},{name},{rub}.{kop}\n')

            # Сохранение счетов, для генерации транзакций ниже.
            accounts.append(f'{account_type},{account_number}')
        # Закрываем файл.
        accounts_file.close()

        ''' Генерация транзакций. '''
        # Открываем файл для чтения в режими дозаписи.
        transactions_file = open(self.__session_transactions_file_path, 'a')
        # Хранение последней сгенерированной даты транзакции.
        last_transaction_date = None
        for _ in range(random.randint(from_number_recodrs, to_number_records)):
            # Генерация новой транзакции в виде строки.
            new_transaction_line = self.generate_transaction(accounts, last_transaction_date=last_transaction_date)

            # Сохранение последней даты транзакции.
            last_transaction_date = datetime.datetime.strptime(new_transaction_line.split(',')[0], '%Y-%m-%d')

            # Запись транзакции в файл.
            transactions_file.write(new_transaction_line)
        # Закрываем файл.
        transactions_file.close()

    def get_last_transaction_date(self):
        """
        Получить дату последней транзакции.

        Returns
        -------
        struct_time
            Последняя дата транзакции.
        """

        last_dates = []

        # Последняя дата из транзакций в очереди.
        if self.__transactions:
            last_dates.append(
                datetime.datetime.strptime(str(self.__transactions[-1].get_transaction_date()), '%Y-%m-%d'))

        # Последняя дата из проведённых транзакций.
        if self.__completed_transactions:
            last_dates.append(
                datetime.datetime.strptime(str(self.__completed_transactions[-1].get_transaction_date()), '%Y-%m-%d'))

        # Если были транзакции, то выбираем самую последнюю дату из них.
        if last_dates:
            return_date = last_dates[0]
            # Для каждой даты из списка проверяем её на наибольшую.
            for last_date in last_dates:
                if last_date > return_date:
                    return_date = last_date
            # Возврат наибольшей даты.
            return return_date

        # Если не было транзакций, возвращаем дату по умолчанию.
        return datetime.datetime.strptime('2012-07-15', '%Y-%m-%d')

    def generate_transaction(
            self,
            accounts=None,
            result_type: str = 'row',
            last_transaction_date=None,
            transaction_amount: str = None,
            transaction_type: str = None
    ):
        """
        Генерация одной транзакции.

        Parameters
        ----------

        result_type : str = 'row'
            Возвращаемый тип транзакции: row - строка для файла, Transaction - экземпляр класса Transaction.

        accounts : list:
            Список счетов, из которых идёт случаяная выборка.

        last_transaction_date : struct_time | None:
            Последняя дата транзакций.

        transaction_amount : str | None:
            Сумма транзакции.

        transaction_type : str(W | D) | None:
            Тип транзакции.

        Returns
        -------

        str | Transaction
            Транзакция в запрашиваемом формате: строка для файла или экземпляр класса транзакции.
        """

        # По умолчанию список существующих счетов.
        if not accounts:
            accounts = self.__accounts_numbers

        # Получить последнюю дату транзакции если неизвестно.
        if not last_transaction_date:
            last_transaction_date = self.get_last_transaction_date()

        # Добавляем к дате последней транзакции 0-1 дней (генерируем новую дату не ранее предыдущей).
        transaction_date = last_transaction_date + datetime.timedelta(days=random.randint(0, 1))
        transaction_date = transaction_date.strftime("%Y-%m-%d")

        # Выбираем случайный тип транзакции.
        if not transaction_type:
            transaction_type = random.choice(self.__transactions_types)

        # Выбираем случайны, ранее сгенерированный и записанный, счёт.
        account_type, account_number = random.choice(accounts).split(',')

        # Генерируем сумму операции (рубли и копейки).
        if not transaction_amount:
            rub = random.randint(1, 10_000)
            kop = random.randint(0, 99)
            transaction_amount = f'{rub}.{kop}'

        # Вывод заданного формата результата.
        if result_type == 'row':
            return f'{transaction_date},{account_type},{account_number},{transaction_type},{transaction_amount}\n'
        else:
            return Transaction(
                transaction_date,
                account_type,
                account_number,
                transaction_type,
                Decimal(transaction_amount)
            )

    def save_accounts_numbers_to_list(self):
        return list(self.__accounts_numbers)

    def save_users_to_list(self):
        return list(self.__users_names)

    def save_users_accounts_to_file(self):
        pass

    def carry_out_random_users_transactions(self, from_random: int, to_random: int):
        # Генерация случайных транзакций.
        for _ in range(random.randint(from_random, to_random)):
            # Генерируем одну транзакцию.
            generated_transaction = self.generate_transaction(self.__accounts_numbers, 'Transaction')
            # Добавляем транзакцию в список.
            self.add_transaction(generated_transaction)

        self.log(f'Сгенерировано {len(self.__transactions)} транзакций.')

        # Проводка сгенерированных транзакций.
        number_carry_out = self.carry_out_transactions()

        self.log(f'Проведено {number_carry_out} транзакций.')

    def log(self, text: str) -> None:
        """ Логирование приложения. """
        if self.__logging:
            print(datetime.datetime.now(), text)

            # Тормозим для красоты вывода.
            if self.__logging_pause:
                sleep(self.__logging_pause)

    def display_monthly_statements(self):
        """ Вывод ежемесячного отчёта по всем счетам. """
        for account in self.__accounts:
            account.display_monthly_statement()
