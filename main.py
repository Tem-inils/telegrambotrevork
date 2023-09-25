import telebot
import buttons
import database
from telebot import types

bot = telebot.TeleBot('6396156210:AAHR0uDD1ZlMrfeKdPAPGebgoGLYm51GW4Q')

users = {}

# database.add_product('apple', 12000, 10, 'Apple the best', 'data:image/jpeg;base64,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')


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
        print(products)

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
        bot.send_message(user_id, f'Вы успешно зарегистрировались {name}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        # Открываем меню
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))

    # если пользователь не отправил контакт
    elif not message.contact:
        bot.send_message(user_id, 'Отправьте контакт с помощью кнопки', reply_markup=buttons.number_buttons())

        # Обратно на этап получения номера
        bot.register_next_step_handler(message, get_number, name)

# Обработчик выбора количества
@bot.callback_query_handler(lambda call: call.data in ['plus', 'minus', 'to_cart', 'back'])
def get_user_product_count(call):
    # Сохраним айди пользователя
    user_id = call.message.chat.id

    # Если пользователь нажал на +
    if call.data == 'plus':
        print(users)
        actual_count = users[user_id]['pr_count']
        print(actual_count)
        print(call)
        users[user_id]['pr_count'] += 1
        # Меняем значение кнопки
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('plus', actual_count))

    # Если пользователь нажал на -
    elif call.data == 'minus':
        print(users)
        actual_count = users[user_id]['pr_count']
        print(actual_count)
        print(call)
        users[user_id]['pr_count'] -= 1
        # Меняем значение кнопки
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('minus', actual_count))

    # back
    # Если пользователь нажал 'назад'
    elif call.data == 'back':
        # Получаем меню
        products = database.get_pr_name_id()
        # меняем на меню
        bot.edit_message_text('Выберите пункт меню',
                              user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu(products))

    # Если нажал Добавить в корзину
    elif call.data == 'to_cart':
        # Получаем данные
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']
        print(users)
        # Добавляем в базу(корзина пользователя)
        database.add_product_to_cart(user_id, user_product, product_count)

        # Получаем обратно меню
        products = database.get_pr_name_id()
        # меняем на меню
        bot.edit_message_text('Продукт добавлен в корзину\nЧто-нибудь еще?',
                              user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu(products))



@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear_cart'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    # Если нажал на кнопку: Оформить заказ
    if call.data == 'order':
        # Удалим сообщение с верхними кнопками
        bot.delete_message(user_id, message_id)
        user_cart = database.get_exact_user_cart(user_id)

        # формируем сообщение со всеми данными
        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        # Итог и Адрес
        full_text += f'\nИтог: {total_amount}'

        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept_kb())
        # Переход на этап подтверждение
        bot.register_next_step_handler(call.message, get_accept,  full_text)

    # Если нажал на кнопку "Корзина"
    elif call.data == 'cart':
        # получим корзину пользователя
        user_cart = database.get_exact_user_cart(user_id)

        # формируем сообщение со всеми данными
        full_text = 'Ваша корзина:\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        # Итог
        full_text += f'\nИтог: {total_amount}'

        # отправляем ответ пользователю
        bot.edit_message_text(full_text,
                              user_id,
                              message_id,
                              reply_markup=buttons.get_cart_kb())

    # Если нажал на очистить корзину
    elif call.data == 'clear_cart':
        # вызов функции очистки корзины
        database.delete_product_from_cart(user_id)

        # отправим ответ
        bot.edit_message_text('Ваша корзина очищена',
                              user_id,
                              message_id,
                              reply_markup=buttons.main_menu_kb(database.get_pr_name_id()))



# функция сохранения статуса заказа
def get_accept(message, full_text):
    user_id = message.from_user.id
    message_id = message.message_id
    user_answer = message.text

    # получим все продукты из базы для кнопок
    products = database.get_pr_name_id()

    # Если пользователь нажал "подтвердить"
    if user_answer == 'Подтвердить':
        admin_id = 302137006
        # очистить корзину пользователя
        database.delete_product_from_cart(user_id)

        # отправим админу сообщение о новом заказе
        bot.send_message(admin_id, full_text.replace("Ваш", "Новый"))

        # отправим ответ
        bot.send_message(user_id, 'Заказ оформлен', reply_markup=types.ReplyKeyboardRemove())

    elif user_answer == 'Отменить':
        # отправим ответ
        bot.send_message(user_id, 'Заказ отменен', reply_markup=types.ReplyKeyboardRemove())

    # Обратно в меню
    bot.send_message(user_id, 'Меню', reply_markup=buttons.main_menu(products))




# Обработчик выбора товара
@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    # Сохраним айди пользователя
    user_id = call.message.chat.id

    # Сохраним продукт во временный словарь
    # call.data - значение нажатой кнопки(инлайн)
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}
    print(users)

    # Сохраним айди сообщения
    message_id = call.message.message_id

    # Поменять кнопки на выбор количества
    bot.edit_message_text('Выберите количество',
                          chat_id=user_id, message_id=message_id,
                          reply_markup=buttons.choose_product_count())




bot.infinity_polling()
