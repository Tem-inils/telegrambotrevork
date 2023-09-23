import telebot

import buttons
import database

bot = telebot.TeleBot('6396156210:AAHR0uDD1ZlMrfeKdPAPGebgoGLYm51GW4Q')

users = {}
database.add_product('apple2', 12000, 10, 'Apple the best', 'Без названия.jfif')


@bot.message_handler(commands=['start'])
def start_message(message):
    # получаем тг ид
    user_id = message.from_user.id

    # Проверка пользователя
    checker = database.check_user(user_id)

    # Если пользователь есть в базе
    if checker:
        # Получаем актуальный список продуктов
        products = database.get_pr_name_id()

        # Отправим сообщение с меню
        bot.send_message(user_id, 'Привет')
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))

    # Если пользователя нету в базе
    elif not checker:
        bot.send_message(user_id, 'Привет отправьте свое имя')

        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получении имени
def get_name(message):
    user_id = message.from_user.id

    # сохранить имю в переменную
    username = message.text

    # Отправим ответ
    bot.send_message(user_id, 'Отправьте свой номер телефона', reply_markup=buttons.number_buttons())
    # перенаправить на этап получения номера
    bot.register_next_step_handler(message, get_number, username)


# получаем номер пользователя
def get_number(message, name):
    user_id = message.from_user.id

    if message.contact:
        # сохраняем контакт
        phone_number = message.contact.phone_number

        # Сохраняем его в базе
        database.register_user(user_id, name, phone_number, 'Not yet')
        bot.send_message(user_id, f'Вы успешно зарегистрировались {name}' + name,
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        # Открываем меню
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))

    # если пользователь не отправил контакт
    elif not message.contact:
        bot.send_message(user_id, 'Отправьте контакт с помощью кнопки', reply_markup=buttons.number_buttons())

        # Обратно на этап получения номера
        bot.register_next_step_handler(message, get_number, name)

# Обработчик выбора кол-во
@bot.callback_query_handler(lambda call: call.data in ['minus', 'plus', 'to_cart', 'back'])
def get_user_product_count(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    # Если пользователь нажал на +
    if call.data == 'plus':
        actual_count = users[user_id]['pr_count']

        users[user_id]['pr_count'] += 1
        # Меняем значения кнопки
        bot.edit_message_reply_markup(user_id, message_id,
                                      reply_markup=buttons.choose_product_count('plus', actual_count))

    # Если пользователь нажал на -
    elif call.data == 'minus':
        print(users)
        actual_count = users[user_id]['pr_count']

        users[user_id]['pr_count'] -= 1
        # Меняем значения кнопки
        bot.edit_message_reply_markup(user_id, message_id,
                                      reply_markup=buttons.choose_product_count('minus', actual_count))


    # Если пользователь нажал 'back'
    elif call.data == 'back':
        # получаем меню
        products = database.get_pr_name_id()
        # меняем на меню
        bot.edit_message_text('Выберите пункт меню', user_id, message_id, reply_markup=buttons.main_menu(products))

    elif call.data == 'to_cart':
        # Получаем данные
        print(users)
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        # Добавляем в базу(корзина пользователя)
        database.add_product_to_cart(user_id, user_product, product_count)

        # получаем меню обратно
        products = database.get_pr_name_id()
        # меняем меню на продукты
        bot.edit_message_text('Продукт добавлен в корзину Что нибудь еще?', user_id, message_id,
                              reply_markup=buttons.main_menu(products)
                              )

# Обработчик выбора товара
@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    # Сохранить айди пользователя
    user_id = call.message.chat.id
    # Cохраним продукт во временный словарь
    # call.data - значения нажатой кнопки(инлайн кнопок)
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}
    # айди сообщения
    message_id = call.message.message_id
    # Поменять кнопки на выбор кол-во
    bot.edit_message_text('Выберите кол-во', user_id, message_id, reply_markup=buttons.choose_product_count())




bot.infinity_polling()
