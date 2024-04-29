import sqlite3
import requests
import telebot
from telebot import types


conn = sqlite3.connect('db/films_db.sqlite', check_same_thread=False)
cursor = conn.cursor()

bot = telebot.TeleBot("6914496932:AAHj7F9AusBjX4c5gqIbjhfsVG1Uy8U7o5Q")


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    """Функция для записи пользователя в БД"""
    cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


def cats():
    """Функция для вывода случайной картинки с кошкой"""
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    image_url = contents[0]['url']
    return image_url


def foxs():
    """Функция для вывода случайной картинки с лисой"""
    contents = requests.get('https://randomfox.ca/floof/').json()
    image_url = contents['link']
    return image_url


def capybaras():
    """Функция для вывода случайной картинки с капибарой"""
    contents = requests.get('https://api.capy.lol/v1/capybara?json=true').json()
    image_url = contents['data']['url']
    return image_url


def dogs():
    """Функция для вывода случайной картинки с собачкой"""
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url


def facts():
    """Функция для вывода случайной цитаты про кошечек"""
    contents = requests.get('https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=1').json()
    factt = contents['text']
    if len(factt) < 10:
        return facts()
    return factt


@bot.message_handler(commands=['start'])
def start_message(message):
    """Приветствие"""
    imgs = open('img/privet2.jpg', 'rb')
    bot.send_photo(message.chat.id, imgs)
    bot.send_message(message.chat.id, 'Вы тут в первый раз?')


@bot.message_handler(commands=['help'])
def start_message(message):
    """Помощь с командами"""
    imgs = open('img/kot.jpeg', 'rb')
    bot.send_photo(message.chat.id, imgs)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text="Кошечки")
    btn2 = types.KeyboardButton(text="Собачки")
    btn3 = types.KeyboardButton(text="Лисички")
    btn4 = types.KeyboardButton(text="Капибары")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, 'Представляю твоему вниманию бота, \n'
                                      'Который поднимет вам настроение различными картинками животных. \n'
                                      'Посмотрите меню, там показаны все животные и факты про кошечек. \n'
                                      'Для вывода картинок с кошками, /cat \n'
                                      'Для вывода картинок с собачками, /dog \n'
                                      'Для вывода картинок с лисички, /fox \n'
                                      'Для вывода картинок с капибары, /capybara \n'
                                      'Для вывода фактов о кошечках, /fact.')


@bot.message_handler(commands=['cat'])
@bot.message_handler(regexp=r'cat')
def meow(message):
    """Случайная фотка кошки"""
    url = cats()
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=['fox'])
@bot.message_handler(regexp=r'fox')
def meow(message):
    """Случайная фотка лисы"""
    url = foxs()
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=['capybara'])
@bot.message_handler(regexp=r'capybara')
def meow(message):
    """Случайная фотка капибары"""
    url = capybaras()
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=['dog'])
@bot.message_handler(regexp=r'dog')
def meow(message):
    """Случайная фотка собачки"""
    url = dogs()
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=['fact'])
@bot.message_handler(regexp=r'fact')
def fact(message):
    """Случайный факт о кошечке"""
    factt = facts()
    bot.send_message(message.chat.id, factt)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """БД"""
    if message.text.lower() == 'да' or message.text.lower() == 'Да'\
            or message.text.lower() == 'ДА'\
            or message.text.lower() == 'дА'\
            or message.text.lower() == 'угу'\
            or message.text.lower() == 'Угу'\
            or message.text.lower() == 'УГу'\
            or message.text.lower() == 'УГУ'\
            or message.text.lower() == 'уГУ'\
            or message.text.lower() == 'угУ'\
            or message.text.lower() == 'уГу'\
            or message.text.lower() == 'УгУ'\
            or message.text.lower() == 'ага'\
            or message.text.lower() == 'Ага'\
            or message.text.lower() == 'АГа'\
            or message.text.lower() == 'АГА'\
            or message.text.lower() == 'АгА'\
            or message.text.lower() == 'аГА'\
            or message.text.lower() == 'агА'\
            or message.text.lower() == 'аГа':
        imgs = open('img/kot2.jpg', 'rb')
        bot.send_photo(message.chat.id, imgs)
        bot.send_message(message.chat.id, 'Ваше имя добавлено в базу данных!\n'
                                          'Ура\n'
                                          'Теперь откройте подсказку\n'
                                          'Для этого нажмите /help')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    elif message.text.lower() == 'нет'\
            or message.text.lower() == 'Нет'\
            or message.text.lower() == 'НЕт'\
            or message.text.lower() == 'НЕТ'\
            or message.text.lower() == 'нЕТ'\
            or message.text.lower() == 'неТ'\
            or message.text.lower() == 'НеТ'\
            or message.text.lower() == 'нЕт'\
            or message.text.lower() == 'не'\
            or message.text.lower() == 'НЕ'\
            or message.text.lower() == 'Не'\
            or message.text.lower() == 'нЕ':
        imgs = open('img/kot5.jpg', 'rb')
        bot.send_photo(message.chat.id, imgs)
        bot.send_message(message.chat.id, 'Тогда нажмите /help,  для подсказки.')


@bot.message_handler(func=lambda m: True)
def repeat(message):
    """Функция для устранения ошибко"""
    if message.text.lower() != 'да' or message.text.lower() != 'Да'\
            or message.text.lower() != 'ДА'\
            or message.text.lower() != 'дА'\
            or message.text.lower() != 'угу'\
            or message.text.lower() != 'Угу'\
            or message.text.lower() != 'УГу'\
            or message.text.lower() != 'УГУ'\
            or message.text.lower() != 'уГУ'\
            or message.text.lower() != 'угУ'\
            or message.text.lower() != 'уГу'\
            or message.text.lower() != 'УгУ'\
            or message.text.lower() != 'ага'\
            or message.text.lower() != 'Ага'\
            or message.text.lower() != 'АГа'\
            or message.text.lower() != 'АГА'\
            or message.text.lower() != 'АгА'\
            or message.text.lower() != 'аГА'\
            or message.text.lower() != 'агА'\
            or message.text.lower() != 'аГа'\
            or message.text.lower() != 'нет'\
            or message.text.lower() != 'Нет'\
            or message.text.lower() != 'НЕт'\
            or message.text.lower() != 'НЕТ'\
            or message.text.lower() != 'нЕТ'\
            or message.text.lower() != 'неТ'\
            or message.text.lower() != 'НеТ'\
            or message.text.lower() != 'нЕт'\
            or message.text.lower() != 'не'\
            or message.text.lower() != 'НЕ'\
            or message.text.lower() != 'Не'\
            or message.text.lower() != 'нЕ':
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
