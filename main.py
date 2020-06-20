import telebot
from telebot import types
import math
import requests
import lxml.html
import threading
import sqlite3
bot = telebot.TeleBot('1253872655:AAGmMEGxoiQ67aa8g_Rj3TNMeXmhQKpg9N8')
sity_cords = {
    'Абакан': '53.720976 91.44242300000001',
    'Архангельск': '64.539304 40.518735',
    'Астана': '71.430564 51.128422',
    'Астрахань': '46.347869 48.033574 ',
    'Барнаул': '53.356132 83.74961999999999',
    'Белгород': '50.597467 36.588849',
    'Бийск': '52.541444 85.219686 ',
    'Бишкек': '42.871027 74.59452 ',
    'Благовещенск': '50.290658 127.527173 ',
    'Братск': '56.151382 101.634152 ',
    'Брянск': '53.2434 34.364198',
    'Великий Новгород': '58.521475 31.275475',
    'Владивосток': '43.134019 131.928379',
    'Владикавказ': '43.024122 44.690476',
    'Владимир': '56.129042 40.40703 ',
    'Волгоград': '48.707103 44.516939 ',
    'Вологда': '59.220492 39.891568',
    'Воронеж': '51.661535 39.200287',
    'Грозный': '43.317992 45.698197 ',
    'Донецк': '48.015877 37.80285 ',
    'Екатеринбург': '56.838002 60.597295',
    'Иваново': '57.000348 40.973921',
    'Ижевск': '56.852775 53.211463 ',
    'Иркутск': '52.286387 104.28066 ',
    'Казань': '55.795793 49.106585 ',
    'Калининград': '55.916229 37.854467',
    'Калуга': '54.507014 36.252277',
    'Каменск-Уральский': '56.414897 61.918905 ',
    'Кемерово': '55.359594 86.08778100000001',
    'Киев': '50.402395 30.532690 ',
    'Киров': '54.079033 34.323163',
    'Комсомольск-на-Амуре': '50.54986 137.007867 ',
    'Королев': '55.916229 37.854467',
    'Кострома': '57.767683 40.926418',
    'Краснодар': '45.023877 38.970157',
    'Красноярск': '56.008691 92.870529',
    'Курск': '51.730361 36.192647',
    'Липецк': '52.61022 39.594719',
    'Магнитогорск': '53.411677 58.984415 ',
    'Махачкала': '42.984913 47.504646',
    'Минск': '53.906077 27.554914 ',
    'Москва': '55.755773 37.617761',
    'Мурманск': '68.96956299999999 33.07454',
    'Набережные Челны': '55.743553 52.39582 ',
    'Нижний Новгород': '56.323902 44.002267',
    'Нижний Тагил': '57.910144 59.98132 ',
    'Новокузнецк': '53.786502 87.155205',
    'Новороссийск': '44.723489 37.76866',
    'Новосибирск': '55.028739 82.90692799999999',
    'Норильск': '69.349039 88.201014',
    'Омск': '54.989342 73.368212 ',
    'Орел': '52.970306 36.063514',
    'Оренбург': '51.76806 55.097449',
    'Пенза': '53.194546 45.019529 ',
    'Первоуральск': '56.908099 59.942935 ',
    'Пермь': '58.004785 56.237654',
    'Прокопьевск': '53.895355 86.744657 ',
    'Псков': '57.819365 28.331786',
    'Ростов-на-Дону': '47.227151 39.744972',
    'Рыбинск': '58.13853 38.573586',
    'Рязань': '54.619886 39.744954',
    'Самара': '53.195533 50.101801 ',
    'Санкт-Петербург': '59.938806 30.314278',
    'Саратов': '51.531528 46.03582 ',
    'Севастополь': '44.616649 33.52536 ',
    'Северодвинск': '64.55818600000001 39.82962',
    'Северодвинск': '64.558186 39.82962 ',
    'Симферополь': '44.952116 34.102411 ',
    'Сочи': '43.581509 39.722882',
    'Ставрополь': '45.044502 41.969065',
    'Сухум': '43.015679 41.025071 ',
    'Тамбов': '52.721246 41.452238',
    'Ташкент': '41.314321 69.267295 ',
    'Тверь': '56.859611 35.911896',
    'Тольятти': '53.511311 49.418084',
    'Томск': '56.495116 84.972128',
    'Тула': '54.193033 37.617752',
    'Тюмень': '57.153033 65.534328 ',
    'Улан-Удэ': '51.833507 107.584125',
    'Ульяновск': '54.317002 48.402243 ',
    'Уфа': '54.734768 55.957838 ',
    'Хабаровск': '48.472584 135.057732 ',
    'Харьков': '49.993499 36.230376 ',
    'Чебоксары': '56.1439 47.248887',
    'Челябинск': '55.159774 61.402455',
    'Шахты': '47.708485 40.215958',
    'Энгельс': '51.498891 46.125121 ',
    'Южно-Сахалинск': '46.959118 142.738068 ',
    'Якутск': '62.027833 129.704151',
}


class Database:
    def __init__(self, db):
        self.db = db

    def check_user(self, user_id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            result = cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, sity, flag):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            result = cursor.execute('INSERT INTO `users` VALUES (?,?,?)', (user_id, sity, flag))

    def get_sity(self, user_id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT `sity` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()

    def update_sity(self, sity, user_id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE `users` SET `sity` = ? WHERE `user_id` = ?', (sity, user_id))

    def sending(self):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT `user_id` FROM `users` WHERE `flag` = ?', (True,))

    def subscribe_sending(self, user_id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE `users` SET `flag` = ? WHERE `user_id` = ?', (True, user_id))

    def unsubscribe_sending(self, user_id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE `users` SET `flag` = ? WHERE `user_id` = ?', (False, user_id))


class Weather:
    def __init__(self, db):
        self.db = db

    def check_sity(self, country):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            result = cursor.execute('SELECT * FROM `weather` WHERE `sity` = ?', (country,)).fetchall()
            return bool(len(result))

    def add_sity(self, sity, weather):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO `weather` VALUES (?,?)', (sity, weather))

    def return_sity(self):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT `sity` FROM `weather`').fetchall()

    def update_weather(self, sity, weather):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE `weather` SET `sity_weather` = ? WHERE `sity` = ?', (weather, sity))

    def return_weather(self, sity):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            for i in cursor.execute('SELECT `sity_weather` FROM `weather` WHERE `sity` = ?', (sity,)):
                for l in i:
                    return l


db = Database('mark-telegram-bot.db')
weather = Weather('mark-telegram-bot.db')


@bot.message_handler(commands=['start'])
def start_weather(message):
    bot.send_message(message.chat.id, 'Определение погоды по местоположению\n'
                                      '/info - информация об всех командах\n'
                                      '/unsubscribe - отписаться от рассылки')
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id,
                     "Отправь мне сво местоположение для определения погоды",
                     reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, 'погода - получить погоду \n' +
                                      'если хочешь сменить город, отправь своё местоположение\n'
                                      '/subscribe - подписаться на рассылку\n'
                                      '/unsubscribe - отписаться от рассылки')


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not db.check_user(str(message.chat.id)):
        bot.send_message(message.chat.id, 'Авторизуйтесь, отправив местоположение')
    else:
        bot.send_message(message.chat.id, 'Вы подписались на рассылку')
        db.subscribe_sending(str(message.chat.id))


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if not db.check_user(str(message.chat.id)):
        bot.send_message(message.chat.id, 'Авторизуйтесь, отправив местоположение')
    else:
        bot.send_message(message.chat.id, 'Вы отписались от рассылки')
        db.unsubscribe_sending(str(message.chat.id))


@bot.message_handler(content_types=['location'])
def send_text(message):
    sity = gett_sity(message.location.latitude, message.location.longitude)
    if not weather.check_sity(sity):
        weather.add_sity(sity, get_weather(sity))
        update_weather()
    if not db.check_user(str(message.chat.id)):
        db.add_user(str(message.chat.id), sity, True)
    else:
        db.update_sity(gett_sity(message.location.latitude, message.location.longitude), message.chat.id)
        sity = db.get_sity(message.chat.id)
        bot.send_message(message.chat.id, f"Текущий город:{sity}")


@bot.message_handler(content_types=['text'])
def send_weather(message):
    if message.text == 'погода':
        if not db.check_user(str(message.chat.id)):
            bot.send_message(message.chat.id, 'Авторизуйтесь, отправив местоположение')
        else:
            for i in db.get_sity(message.chat.id):
                bot.send_message(message.chat.id, weather.return_weather(i))


def location(latt1, lonng1, latt2, lonng2):
    rad = 6372795
    llat1 = latt1
    llong1 = lonng1
    llat2 = latt2
    llong2 = lonng2
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    return round(dist)


def get_weather(name):
    print(name)
    tree = lxml.html.document_fromstring(requests.get(f'https://www.google.com/search?q=погода+в+{name}&sourceid=chrome&ie=UTF-8',
                                                      headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}).text,)
    temp = tree.xpath("//*[@id='wob_tm']/text()")[0]
    water = tree.xpath("//*[@id='wob_hm']/text()")[0]
    wind = tree.xpath('//*[@id="wob_ws"]/text()')[0]
    return f"температура: {temp} \nвлажность: {water} \nветер:{wind}"


def gett_sity(lat, long):
    meters = 100000000000
    sity = ''
    for t, lon in sity_cords.items():
        loc = location(lat, long, round(float(lon.split()[0]), 3), round(float(lon.split()[1]), 3))
        if loc < meters:
            meters = loc
            sity = t
    return sity


def sending_message():
    for i in db.sending():
        for l in i:
            for e in db.get_sity(l):
                bot.send_message(l, weather.return_weather(e))


def update_weather():
    for i in weather.return_sity():
        for l in i:
            weather.update_weather(l, get_weather(l))
    sending_message()
    timer = threading.Timer(10800, update_weather)
    timer.start()


update_weather()
bot.polling()