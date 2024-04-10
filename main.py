import telebot
from telebot import types
import sqlite3
import random
import requests
import json

bot = telebot.TeleBot('7087078113:AAH60Sn3ksr61g17aPQSUNZ1wdWdO3NWLj4')

def help_handler(message):
    chat_id = message.chat.id



@bot.message_handler(commands=['start'])
def tab(message):
    with sqlite3.connect('Data.sql') as connect:
        cursor = connect.cursor()
    SQL_SCRIPT = """
            CREATE TABLE IF NOT EXISTS 
            users(
            id int auto_increment primary key, 
            high varchar(50), 
            weight varchar(50)
            )
            """
    cursor.execute(SQL_SCRIPT)
    connect.commit()
    bot.send_message(message.chat.id, 'Привет, сейчас мы тебя зарегестрируем! введи свой рост и вес (в строчку через пробел)')
    bot.register_next_step_handler(message, user_h)

def user_h(message):
    h = str(message.text)
    ls = list(map(int, h.split()))
    imt = (ls[1] / ((ls[0] / 100) ** 2))
    if imt >= 18.5 and imt <= 25:
        bot.send_message(message.chat.id, 'У тебя хорошее отношение роста и веса. Если тебя устраивает вид своего тела в зеркале, то можешь чилить. Если нет, то используй кнопки ниже')
    if imt < 18.5:
        bot.send_message(message.chat.id, 'Ты хиленький бро. Надо набрать массу и подкачаться')
    if imt > 25:
        bot.send_message(message.chat.id, 'Ты жирный бро. Надо худеть')
    with sqlite3.connect('Data.sql') as connect:
        cursor = connect.cursor()
        SQL_SCRIPT = f"""
            INSERT INTO
            users(
            high, weight
            )
            VALUES (
            '%s', '%s'
            )
            """ % (ls[0], ls[1])
        cursor.execute(SQL_SCRIPT)
        connect.commit()
        cursor.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

    printer(message)

@bot.message_handler(commands=['start'])
def printer(message):
    mark = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Как набрать масcу?')
    btn2 = types.KeyboardButton('Как похудеть?')
    btn3 = types.KeyboardButton('Как накачаться?')
    mark.add(btn1)
    mark.add(btn2)
    mark.add(btn3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Этот бот бесплатно предоставит тебе программу тренировок для того, чтобы твоё тело достигло своей пиковой формы и пика своих возможностей. Удачных тренировок бро :)')
    file = open('./preview.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=mark)
    bot.register_next_step_handler(message, back)
def back(message):
    if message.text == 'Как набрать масcу?':
        bot.send_photo(message.chat.id, open('./IMG_1055.jpg', 'rb'))
    elif message.text == 'Как похудеть?':
        bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=4PDNcUmr9ls')
        bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=3bbQ2JJDJ60&t=11s')
        bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=HqGNizXiQIg')
    elif message.text == 'Как накачаться?':
        bot.send_message(message.chat.id, 'https://www.wildberries.ru/catalog/206170257/detail.aspx?utm_referrer=https%3A%2F%2Fyandex.ru%2Fproducts%2Fsearch%3Ftext%3D%25D0%25BA%25D1%2583%25D0%25BF%25D0%25B8%25D1%2582%25D1%258C%2520%25D1%2581%25D1%2582%25D0%25B5%25D1%2580%25D0%25BE%25D0%25B8%25D0%25B4%25D1%258B%2520%25D0%25B4%25D0%25BB%25D1%258F%2520%25D0%25BD%25D0%25B0%25D0%25B1%25D0%25BE%25D1%2580%25D0%25B0%2520%25D0%25BC%25D1%258B%25D1%2588%25D0%25B5%25D1%2587%25D0%25BD%25D0%25BE%25D0%25B9%2520%25D0%25BC%25D0%25B0%25D1%2581%25D1%2581%25D1%258B')
        bot.send_message(message.chat.id, 'А если серьёзно, начни регулярно ходить в зал (и хотя бы полгода походи в зал с тренером, чтобы он тебе обьяснил что и как в зале). Также употребляй много белка. А вообще, вещица сверху ☝️  - очень осуждаемая штука в обществе качков. Я тебе тоже не советую употреблять стероиды и рисковать своим здоровьем ради мышц ✌️')
    bot.register_next_step_handler(message, back)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    with sqlite3.connect('Data.sql') as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users')
        users_list = cursor.fetchall()

        info = ''
        users_counter = 0
        for n, el in enumerate(users_list):
            info += f'(USER_{n + 1}:  Рост: {el[1]};\n Вес: {el[2]};\n id Пользователя: 186745{random.randrange(1, 1000)})\n'
            users_counter += 1
    bot.send_message(call.message.chat.id, info)
    bot.send_message(call.message.chat.id, f'Всего этот бот использовало {len(users_list)} человек')


@bot.message_handler(commands=['mentality'])
def video(message):
    text = ('https://www.youtube.com/watch?v=aX98yu_1doE')
    bot.send_message(message.chat.id, text)


API = 'a165a3f4ce09e6b7c4c4d4ed4cd43dfa'
@bot.message_handler(commands=['weather'])
def survey(message):
    bot.send_message(message.chat.id, 'Привет!, рад тебя видеть! Напиши название города ')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().capitalize()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        dt = json.loads(res.text)
        bot.reply_to(message, f"""Сейчас погода в '{city}': {dt["main"]["temp"]}°С""")

    else:
        bot.reply_to(message, f'Братиш, ты что пьяный? Нет такого города. ')


bot.polling(non_stop=True)

