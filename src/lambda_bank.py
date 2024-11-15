import random
from datetime import datetime
from time import sleep

from src import reader


class LambdaBank:
    """ Основной класс для запуска приложения. """

    def __init__(self, logging: bool = True, logging_pause: int = 1):
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
        self.__title = 'Лямбда Банк'  # Название приложения.

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

        # Пути для файлов данных.
        self.__original_accounts_file_path = 'database/original/accounts.csv'  # Оригинальный файл данных счетов.
        self.__original_transactions_file_path = 'database/original/transactions.csv'  # Оригинальный файл данных транзакций.
        self.__session_accounts_file_path = 'database/session/accounts.csv'  # База данных счетов сессии приложения.
        self.__session_transactions_file_path = 'database/session/transactions.csv'  # Оригинальный файл данных транзакций.

        # Настройки логирования.
        self.__logging = logging
        self.__logging_pause = logging_pause

        # Существующие аттрибуты класса.
        self.__accounts = None
        self.__all_accounts_numbers = None
        self.__all_users_names = None
        self.__transactions = None

    def start(self):
        self.log(f'λ Старт приложения "{self.__title}".')
        self.prepare_session_files()

        return True  # TODO Temp.

        # Получаем список счетов.
        self.log('↻ Формирование списка счетов из файла.')
        self.__accounts, self.__all_accounts_numbers, self.__all_users_names = reader.read_accounts(
            self.__accounts_file_path)
        self.log(
            f'! В файле счетов найдено {len(self.__accounts)} строк, номеров счетов: {len(self.__all_accounts_numbers)}, ФИО: {len(self.__all_users_names)}.')

        # Получаем список транзакций.
        self.log('↻ Формирование списка транзакций из файла.')
        self.__transactions = reader.read_transactions(self.__transactions_file_path)
        self.log(f'! В файле транзакций найдено {len(self.__transactions)} строк.')

        # Проводим все транзакции по счетам.
        self.log('↻ Проводка транзакций по счетам пользователей.')
        self.carry_out_transactions()

    def prepare_session_files(self):
        reader.copy_file(self.__original_accounts_file_path, self.__session_accounts_file_path)
        reader.copy_file(self.__original_transactions_file_path, self.__session_transactions_file_path)

    def restart(self):
        self.start()

    def carry_out_transactions(self):
        pass

    def generate_files_records(self, from_number_recodrs: int, to_number_records: int):
        """ Генерация данных: счетов и транзакций. """

        # Создаём словарь для генерации с весом.
        letters = {
            'q': 10, 'w': 10, 'e': 90, 'r': 30, 't': 20, 'y': 90, 'u': 90, 'i': 90, 'o': 90, 'p': 20,
            'a': 90, 's': 20, 'd': 40, 'f': 30, 'g': 20, 'h': 50, 'j': 30, 'k': 30, 'l': 20, 'z': 10,
            'x': 10, 'c': 50, 'v': 30, 'b': 80, 'n': 80, 'm': 70,
        }
        # Получаем списки для генерации.
        letter_keys = list(letters.keys()) # Список букв.
        letter_values = list(letters.values()) # Список веса для генератора.

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
        transaction_day = 16
        for _ in range(random.randint(from_number_recodrs, to_number_records)):
            # Добавляем к дате транзакции 0-1 дней (генерируем новую дату не ранее предыдущей).
            transaction_day += random.randint(0, 1)
            transaction_date = f'2012-07-{transaction_day}'

            # Выбираем случайный тип транзакции.
            transaction_type = random.choice(self.__transactions_types)

            # Выбираем случайны, ранее сгенерированный и записанный, счёт.
            account_type, account_number = random.choice(accounts).split(',')

            # Генерируем сумму операции (рубли и копейки).
            rub = random.randint(1, 10_000)
            kop = random.randint(0, 99)

            # Запись транзакции в файл.
            transactions_file.write(f'{transaction_date},{transaction_type},{account_number},{account_type},{rub}.{kop}\n')
        # Закрываем файл.
        transactions_file.close()

    def save_accounts_numbers_to_list(self):
        pass

    def save_users_to_list(self):
        pass

    def save_users_accounts_to_file(self):
        pass

    def carry_out_random_users_transactions(self):
        pass

    def log(self, text: str) -> None:
        """ Логирование приложения. """
        if self.__logging:
            print(datetime.now(), text)

            # Тормозим для красоты вывода.
            if self.__logging_pause:
                sleep(self.__logging_pause)
