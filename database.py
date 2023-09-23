import sqlite3

from datetime import datetime

db = sqlite3.connect('dostavka.db')

fake_evos = db.cursor()

# Создание таблицы пользователя
fake_evos.execute('CREATE TABLE IF NOT EXISTS users'
                  '(tg_id INTEGER, name TEXT, phone_number TEXT, address TEXT,'
                  'reg_date DATETIME);')

# Ваш код для создания таблицы не изменяется
fake_evos.execute('CREATE TABLE IF NOT EXISTS user_cart'
                  '(user_id INTEGER, user_product TEXT, quantity INTEGER,'
                  'total_for_product REAL);')  # добавил столбец total_for_product


# Создание таблицы для корзины пользователя
fake_evos.execute('CREATE TABLE IF NOT EXISTS user_cart'
                  '(user_id INTEGER, user_product TEXT, quantity INTEGER,'
                  'total_for_price REAL);')


# Регистрация пользователя
def register_user(tg_id, name, phone_number, address):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    # Добавляем пользователя в базу данных
    fake_evos.execute('INSERT INTO users (tg_id, name, phone_number, address, reg_date) VALUES '
                      '(?, ?, ?, ?, ?);', (tg_id, name, phone_number, address, datetime.now()))

    db.commit()


# Проверяем пользователя есть ли такой id в нашем базе данных
def check_user(user_id):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    checker = fake_evos.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False


# Добавления продукта в таблицу products
def add_product(pr_name, pr_price, pr_quantity, pr_des, pr_photo):
    db = sqlite3.connect('dostavka.db')
    fake_evos = db.cursor()

    fake_evos.execute('INSERT INTO products'
                      '(pr_name, pr_price, pr_quantity, pr_des, pr_photo, reg_date) VALUES'
                      '(?, ?, ?, ?, ?, ?);', (pr_name, pr_price, pr_quantity, pr_des, pr_photo, datetime.now()))

    db.commit()
    db.close()  # Закрываем соединение



# Получаем все продукты из базы только его (name, id)
def get_pr_name_id():
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    products = fake_evos.execute('SELECT pr_name, pr_id, pr_quantity FROM products;').fetchall()
    sorted_products = [(i[0], i[1]) for i in products if i[2] > 0]

    return sorted_products


def get_pr_id():
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    products = fake_evos.execute('SELECT pr_name, pr_id, pr_quantity FROM products;').fetchall()
    sorted_products = [(i[1]) for i in products if i[2] > 0]

    return sorted_products


# Получить информацию про определенный продукт через его pr_id
def get_product_id(pr_id):
    db = sqlite3.connect('dostavka.db')
    fake_evos = db.cursor()

    product_id = fake_evos.execute('SELECT pr_name, pr_des, pr_photo, pr_price '
                                   'FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    return product_id



# Добавления продуктов в корзину
def add_product_to_cart(user_id, user_product, quantity):
    db = sqlite3.connect('dostavka.db')
    fake_evos = db.cursor()

    product_info = get_product_id(user_product)
    if product_info:
        product_price = product_info[3]
        fake_evos.execute('INSERT INTO user_cart '
                          '(user_id, user_product, quantity, total_for_product) '
                          'VALUES (?, ?, ?, ?);', (user_id, user_product, quantity, quantity * product_price))
        db.commit()
    else:
        print(f"Продукт с ID {user_product} не найден.")



# Удаление продуктов из корзины
def delete_product_from_cart(pr_id, user_id):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    # Удалить продукт из корзины через pr_id(продукт айди)
    fake_evos.execute('DELETE FROM user_cart WHERE user_product=? AND user_id=?;', (pr_id, user_id))

    db.commit()
