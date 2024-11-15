from src.lambda_bank import LambdaBank

# Получаем экземпляр класса приложения.
lambda_bank = LambdaBank()

# 1. Запустить приведенную программу.
lambda_bank.start()

# 2. Добавить в каждый файл 5-8 записей и проверить работу.
lambda_bank.generate_files_records(5, 8)
lambda_bank.carry_out_transactions() # TODO.

# 3. Сохранить счета и пользователей в виде списков.
lambda_bank.save_accounts_numbers_to_list()
lambda_bank.save_users_to_list()

# 4. Для пользователей сохраненных в виде списков провести 10-15 транзакций различного вида вывести результат на экран.
lambda_bank.carry_out_random_users_transactions()

# 5. Добавить метод сохранения списка счетов в файл.
lambda_bank.save_users_accounts_to_file()

# 6. Добавить лимиты по счетам: минимальный и максимальный остаток и при отслеживание лимитов при проведении транзакций.
