from clickhouse_driver import Client
import time


def check_table_exists(client, table_name):
    query = f"EXISTS TABLE {table_name}"
    try:
        return client.execute(query)[0][0]  # Возвращает True или False
    except:
        print(f"Error checking table")
        return False


table_name = "table_dataset1"
client = Client(host="clickhouse", port=9000, user="default", password="", database="default")

# Проверяем доступность таблицы с интервалом в 5 секунд
while True:
    if check_table_exists(client, table_name):
        print(f"Таблица {table_name} доступна.")
        break
    else:
        print(f"Таблица {table_name} недоступна, пробую снова через 5 секунд...")
        time.sleep(5)


print("CONNECT!")
query = "SELECT * FROM table_dataset1 LIMIT 10"
result = client.execute(query)

# Вывод результатов
for row in result:
    print(row)

print("Generate@")

# Извлекаем уникальные email из первой таблицы
emails = client.execute("SELECT DISTINCT email FROM table_dataset1")

# Итеративно извлекаем uid из каждой таблицы
for email in emails:
    email = email[0]

    uid1 = client.execute(f"SELECT uid FROM table_dataset1 WHERE email = '{email}'")
    uid2 = client.execute(f"SELECT uid FROM table_dataset3 WHERE email = '{email}'")

    # Если uid найден, добавляем их в новую таблицу
    if uid1 and uid2:
        client.execute(
            "INSERT INTO table_results (id_is1, id_is2, id_is3) VALUES", [([uid1[0][0]], [uid2[0][0]], [uid2[0][0]])]
        )
        print("Add new row")

print("Данные успешно записаны в новую таблицу.")
