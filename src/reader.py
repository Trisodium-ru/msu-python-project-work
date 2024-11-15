from decimal import Decimal

from src.current_account import CurrentAccount
from src.saving_account import SavingAccount
from src.transcation import Transaction


def read_transactions(filename: str, delimeter: str = ',') -> [Transaction]:
    """
    Чтение транзакций из файла.

    Parameters
    ----------
    filename : str
        Путь к файлу для чтения.

    delimeter: str
        Разделитель полей строки в файле. По умолчанию - запятая.

    Returns
    ----------
    [Transaction]
        Список считанных транзакций из файла в виде списка классов Transaction.
    """
    # Открываем файл для чтения.
    transaction_file = open(filename, 'r')
    # Создаём список транзакций для заполнения и возврата.
    transactions = list()

    # Читаем файл по одной строке для экономии памяти.
    while transaction_line := transaction_file.readline():
        # Получаем список данных строки.
        transaction_fields = get_line_fields(transaction_line, delimeter)
        # Создаём транзакцию из полей строки. Последнее поле - сумма, сразу создаём числовой класс.
        transaction = Transaction(
            transaction_fields[0],  # Дата транзакции.
            transaction_fields[1],  # Тип счёта.
            transaction_fields[2],  # Номер счёта.
            transaction_fields[3],  # Тип операции.
            Decimal(transaction_fields[4])  # Сумма операции.
        )
        # Добавляем созданный класс транзакции в список.
        transactions.append(transaction)

    # Закрываем файл.
    transaction_file.close()
    
    # Возвращаем результат (список транзакций).
    return transactions


def read_accounts(filename: str, delimeter: str = ',') -> [CurrentAccount | SavingAccount]:
    """
    Чтение банковских счетов из файла.

    Parameters
    ----------
    filename : str
        Путь к файлу для чтения.

    delimeter: str
        Разделитель полей строки в файле. По умолчанию - запятая.

    Returns
    ----------
    ([CurrentAccount | SavingAccount], {str}, {str})
        Возвращает кортеж:
            1. Список считанных банковских счетов из файла в виде списка экземпляров классов CurrentAccount или SavingAccount;
            2. Все номера банковских аккаунтов (множество).
            3. Все ФИО клиентов банка (множество).
    """
    # Открываем файл для чтения.
    accounts_file = open(filename, 'r')
    # Создаём список транзакций для заполнения и возврата.
    accounts = list()
    # Создаём множества для пользователей и счетов.
    all_accounts_numbers, all_users_numbers = set(), set()

    # Читаем файл по одной строке для экономии памяти.
    while account_line := accounts_file.readline():
        # Получаем список данных строки.
        account_fields = get_line_fields(account_line, delimeter)

        # Создаём переменные для понимания полей (человеком).
        account_type = account_fields[0]  # Тип счёта.
        account_number = account_fields[1]  # Номер счёта.
        user_name = account_fields[2]  # ФИО пользователя.
        balance = Decimal(account_fields[3])  # Баланс на счету.

        # Добавляем ФИО, номера счетов пользователей в списки.
        all_accounts_numbers.add(account_fields[1])
        all_users_numbers.add(account_fields[2])

        # В зависимости от типа счёта создаются разные классы счёта.
        match account_type:
            case 'S':  # Сберегательный счёт.
                account = SavingAccount(account_number, user_name, balance)
            case 'C':  # Текущий счёт.
                account = CurrentAccount(account_number, user_name, balance)
            case _:
                exit(f'Ошибка 96: неизвестный тип счёта в файле "{filename}"')

        # Добавляем экземпляр класса счёта в общий список.
        accounts.append(account)

    # Закрываем файл.
    accounts_file.close()

    # Возвращаем результат.
    return accounts, all_accounts_numbers, all_users_numbers


def get_line_fields(line: str, delimeter: str) -> list:
    # Чистим переносы строк и пробелы по краям, разбиваем строку на список полей по заданному разделителю.
    return line.strip().split(delimeter)


def copy_file(from_path: str, to_path: str) -> None:
    # Открываем файлы для копирования.
    from_file = open(from_path, 'r') # Режим чтения.
    to_file = open(to_path, 'w') # Режим записи.

    # Построчно копируем файл.
    while from_file_line := from_file.readline():
        to_file.write(from_file_line)

    # Закрываем файлы после копироваания.
    from_file.close()
    to_file.close()
