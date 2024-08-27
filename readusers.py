import sqlite3

# Подключаемся к базе данных SQLite
db_path = 'users.db'

try:
    # Создаем соединение с базой данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Пример запроса: получаем все таблицы из базы данных
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Таблицы в базе данных:")
    for table in tables:
        print(table[0])

    # Пример запроса: получаем все записи из таблицы users
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    print("\nДанные из таблицы users:")
    for row in rows:
        print(row)

    # Закрываем соединение
    conn.close()
except sqlite3.Error as e:
    print(f"Произошла ошибка при работе с базой данных: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")