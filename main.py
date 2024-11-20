from src.lambda_bank import LambdaBank

# Получаем экземпляр класса приложения.
lambda_bank = LambdaBank(True) # True, 1

# 1. Запустить приведенную программу.
print('1. Запустить приведенную программу.')
lambda_bank.start()
print()

# 2. Добавить в каждый файл 5-8 записей и проверить работу.
print('2. Добавить в каждый файл 5-8 записей и проверить работу.')
# 2.1. Добавление записей.
lambda_bank.generate_files_records(5, 8)
# 2.2. Проверка работы (проводка транзакций из файла).
lambda_bank.carry_out_transactions_from_file()
print()

# 3. Сохранить счета и пользователей в виде списков.
print('3. Сохранить счета и пользователей в виде списков.')
# 3.1. Сохранение счетов в виде списков.
account_numbers = lambda_bank.save_accounts_numbers_to_list()
print('Список счетов: ', account_numbers)
# 3.2. Сохранение пользователей в виде списков.
users_names = lambda_bank.save_users_to_list()
print('Список пользователей: ', users_names)
print()

# 4. Для пользователей сохраненных в виде списков провести 10-15 транзакций различного вида вывести результат на экран.
print('4. Для пользователей сохраненных в виде списков провести 10-15 транзакций различного вида вывести результат на экран.')
# 4.1. Генерация и проводка 10-15 транзакций.
lambda_bank.carry_out_random_users_transactions(10, 15)
# 4.2. Вывод результата на экран.
lambda_bank.display_monthly_statements()
print()

# 5. Добавить метод сохранения списка счетов в файл.
print('5. Добавить метод сохранения списка счетов в файл.')
lambda_bank.save_users_accounts_to_file()
print()

# 6. Добавить лимиты по счетам: минимальный и максимальный остаток и отслеживание лимитов при проведении транзакций.
print('6. Добавить лимиты по счетам: минимальный и максимальный остаток и отслеживание лимитов при проведении транзакций.')
# 6.1. Генерируем транзакцию с большой суммой для проверки лимитов
big_transaction = lambda_bank.generate_transaction(result_type='Transaction', transaction_amount='20000.00', transaction_type='W')
# 6.2. Добавляем транзакцию в список обработки.
lambda_bank.add_transaction(big_transaction)
# 6.3. Проводим сгенерированную транзакцию.
lambda_bank.carry_out_transactions()
print()
