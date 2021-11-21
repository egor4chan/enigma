import sqlite3
from aiogram.types import user
import bot as b

def create_database():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        refer INTEGER,
        ref INTEGER,
        balance INTEGER,
        follow_status INTEGER
    )""")
    db.commit()


def add_collumn():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute("ALTER TABLE users ADD COLUMN followed_status;")
    db.commit()

def check_in_db(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None: # если айди нет в БД
        return False
    else:
        return True

def add_to_db(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"""INSERT INTO users (user_id) VALUES ('{user_id}');""") # добавляем значение в поле USER ID
    db.commit()

def set_refer(refer_id, user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"""INSERT INTO users (refer, user_id, balance, followed_status) VALUES ('{refer_id}', '{user_id}', 0, 0)""") # добавляем значение в поле REFER
    db.commit()

def my_refs(user):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT refer FROM users WHERE refer = '{user}'")
    list_all = cursor.fetchall()
    all_l = len(list_all)
    return all_l


def get_all_users():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("""SELECT user_id FROM users""")
    all_users = cursor.fetchall()
    return len(all_users)

def clear_table():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE user_id IS NULL or user_id = '' ")
    db.commit()


def get_top():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    balances_list = []
    cursor.execute("SELECT balance FROM users")
    balances = cursor.fetchall()
    for i in range(len(balances)):
        balances_list.append(int(balances[i][0]))
    print(max(balances_list))


def getBalance(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
    balance_id = cursor.fetchall()[0][0]
    return balance_id




def balance_up(user, count):
    # count - количество, которое добавится к балансу
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT balance FROM users WHERE user_id = '{user}'") # выбираем ячейку БАЛАНС
    balance_before = cursor.fetchone()[0]
    balance_upped = int(balance_before) + int(count)
    cursor.execute(f"UPDATE users SET balance = '{balance_upped}' WHERE user_id = '{user}'") # Обновляем значение БАЛАНС ++
    db.commit()


def balance_down(user, count):
    # count - количество, которое добавится к балансу
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE user_id = '{user}'") # выбираем ячейку БАЛАНС
    balance_before = cursor.fetchone()[0]
    balance_upped = int(balance_before) - int(count)
    cursor.execute(f"UPDATE users SET balance = '{balance_upped}' WHERE user_id = '{user}'") # Обновляем значение БАЛАНС ++
    db.commit()

def select_users():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("SELECT user_id FROM users")
    items = cursor.fetchall() # Все юзеры
    return items

def in_channel(user):
    user_channel_status = bot.get_chat_member(chat_id='@enigma_prod', user_id=user)
    if user_channel_status["status"] != 'left':
        return True # в группе состоит
    else:
        return False # если человек не в группе

def get_status(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    status = cursor.execute(f"SELECT status FROM users WHERE user_id = '{user_id}'").fetchone()

    print(status[0])

def print_my_refs(refer_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT user_id FROM users WHERE refer = '{refer_id}'")
    refs = cursor.fetchall()
    refs_len = len(refs)


    for ref in range(refs_len):
        res = refs[ref][0]
    return res

def username(user_id): # возвращаем никнейм
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT username FROM users WHERE user_id = '{user_id}'")
    username = cursor.fetchone()
    return username[0]

def set_username(user_id, username): # Проверка наличия никнейма
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"UPDATE users SET username = '{username}' WHERE user_id = '{user_id}'")
    db.commit()

def second_refer(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT refer FROM users WHERE user_id = '{user_id}'") # ВЫБОР рефера ПОЛЬЗОВАТЕЛЯ
    refer = cursor.fetchone()[0]

    cursor.execute(f"SELECT refer FROM users WHERE user_id = '{refer}'")
    second_refer = cursor.fetchone()[0]

    if third_refer != '0':
        return second_refer
    else:
        return '0'

def third_refer(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT refer FROM users WHERE user_id = '{user_id}'") # ВЫБОР рефера ПОЛЬЗОВАТЕЛЯ
    refer = cursor.fetchone()[0]

    cursor.execute(f"SELECT refer FROM users WHERE user_id = '{refer}'")
    second_refer = cursor.fetchone()[0]

    cursor.execute(f"SELECT refer FROM users WHERE user_id = '{second_refer}'")
    third_refer = cursor.fetchone()[0]
    if third_refer != '0':
        return third_refer
    else:
        return '0'


def in_status_database(user_id): # Добавляем в базу если нет
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT user_id FROM status WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None: # если айди нет в БД
        return False
    else:
        return True

def register_user(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"""INSERT INTO status (user_id) VALUES ('{user_id}');""") # добавляем значение в поле USER ID
    db.commit()

def qiwi_status(user_id): # узнаем статус нажатия киви
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT qiwi_status FROM status WHERE user_id = '{user_id}'")
    qiwi_status = cursor.fetchone()[0]
    return qiwi_status

def update_qiwi_status(user_id, value):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"UPDATE status SET qiwi_status = '{value}' WHERE user_id = '{user_id}'")
    db.commit()



def register_number(user_id, number):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT number FROM users WHERE user_id = '{user_id}'")
    selected_number = cursor.fetchone()[0]


    result_number = number.replace('+', '')
    if len(result_number) == 11:
        cursor.execute(f"UPDATE users SET number = '{result_number}' WHERE user_id = '{user_id}'")
        db.commit()
        return 'success'
    else:
        return 'error'

def return_number(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT number FROM users WHERE user_id = '{user_id}'")
    selected_number = cursor.fetchone()[0]

    if selected_number == 0:
        return 'none'
    else:
        return 'true'

def get_number(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT number FROM users WHERE user_id = '{user_id}'")
    selected_number = cursor.fetchone()[0]
    return selected_number


def add_check(user_id, money, bill_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("INSERT INTO 'check' ('user_id', 'money', 'bill_id') VALUES (?, ?, ?)", (user_id, money, bill_id,))

def get_check(bill_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    result = cursor.execute("SELECT * FROM 'check' WHERE 'bill_id' = ?", (bill_id,)).fetchmany(1)
    if not bool(len(result)):
        return False
    return result[0]


def delete_check(bill_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    return cursor.execute("DELETE FROM 'check' WHERE bill_id = (?)", (bill_id,))
    db.commit()

def set_status(user_id, status):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"UPDATE users SET status = '{status}' WHERE user_id = '{user_id}'")
    db.commit()

def return_status(user_id):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    status = cursor.execute(f"SELECT status FROM users WHERE user_id = '{user_id}'").fetchone()[0]
    if status == 0:
        return 'неактивен'
    else:
        return 'активен'



def get_refs(user):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT user_id FROM users WHERE refer = '{user}'")
    users = cursor.fetchall()
    if users != '':
        return users # вернуть список рефов по айди
    else:
        return ''
