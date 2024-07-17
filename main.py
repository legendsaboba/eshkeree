import requests
import telebot
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
from random import randint
import os
import pygame

session = {}
load_dotenv(find_dotenv())
token = os.getenv('token')

bot = telebot.TeleBot(token, parse_mode='HTML')
@bot.message_handler(commands=['weather'])
def weather(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    key = KeyboardButton(text = 'отправить геопозицию', request_location=True)
    markup.add(key)
    bot.send_message(chatID, 'пожалуйста отправьте геопозицию', reply_markup=markup)
    bot.register_next_step_handler(message, weather1)
def weather1(message):
    chatID = message.from_user.id
    buttons2(message)
    lat = message.location.latitude
    lon = message.location.longitude
    current_weather = get_temp(lat, lon)
    bot.send_message(chatID, f'Текущая темперптура:{current_weather}')



def get_temp(lat, lon):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}.52&longitude={lon}.41&current=temperature_2m,cloud_cover,wind_speed_10m&hourly=temperature_2m'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_temp = str(data['current']['temperature_2m'])
        return current_temp
    else:
        print(f'ошибка: {response.status_code}')
        return 'не удалось определить погоду'

@bot.message_handler(commands=['game'])
def game(message):
    chatID = message.from_user.id
    bot.send_message(chatID, 'вы готовы?')
    bot.register_next_step_handler(message, game1)
def game1(message):
    chatID = message.from_user.id
    if 'не' in message.text.lower():
        bot.send_message(chatID, 'напишите как будете готовы')
    else:
        bot.send_message(chatID, 'введите число и я отгадаю его')
        bot.register_next_step_handler(message, game2)

@bot.message_handler(commands=['word'])
def word(message):
    bot.send_message(message.chat.id, 'введите слово')
    bot.register_next_step_handler(message, get_info_word)

def get_info_word(message):
    url = f'https://ru.wiktionary.org/wiki/{message.text.lower()}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answer = soup.find('ol')
    bot.send_message(message.chat.id, f'{message.text} - {answer.text}')

def get_anecdot():
    url = f'https://www.anekdot.ru/last/anekdot/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answer = soup.findAll('div', class_ = 'text')
    try:
        answer = get_anecdot()
        bot.send_message(message.chat.id, answer[randint(0, len(answer))].text)
    except:
        bot.send_message(message.chat.id, 'извините я вас не понял')

def game2(message):
    chatID = message.from_user.id
    try:
        number = int(message.text)
        bot.send_message(chatID, number)
    except:
        bot.send_message(chatID, 'надо ввести только число')
        bot.register_next_step_handler(message, game2)

@bot.message_handler(commands=['anketa'])
def start_anketa(message):
    chatID = message.from_user.id
    bot.send_message(chatID, 'введите ваше имя')
    bot.register_next_step_handler(message, anketa1)

def anketa1(message):
    chatID = message.from_user.id
    try:
        session[chatID]['name'] = message.text
        bot.send_message(chatID, 'введите ваш возраст')
        bot.register_next_step_handler(message, anketa2)
    except:
        bot.send_message(chatID, 'возможно вы не ввели команду /start')

def anketa2(message):
    chatID = message.from_user.id
    if 'не' in message.text.lower():
        bot.send_message(chatID, 'ну и ладно')
    else:
        try:
            session[chatID]['age'] = int(message.text)
        except:
            bot.send_message(chatID, 'введите ваш возраст числом')
            bot.register_next_step_handler(message, anketa2)


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    chatID = callback.message.from_user.id
    button_call = callback.data
    if button_call == 'button1':
        bot.send_photo(chatID, 'https://s0.rbk.ru/v6_top_pics/media/img/5/31/756806793338315.png')
    elif button_call == 'button2':
        bot.send_photo(chatID, open('nasa-black-hole-visualization-1.gif', 'rb'))
    elif button_call == 'button3':
        bot.send_document(chatID, open('dfdfsdfdfsf.txt', 'rb'))

@bot.message_handler(commands=['buttons'])
def buttons(message):
    chatID = message.from_user.id
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('фото', callback_data='photo')
    button2 = InlineKeyboardButton('гифка', callback_data='gif')
    button3 = InlineKeyboardButton('текст', callback_data='doc')
    markup.add(button1,button2,button3)
    bot.send_message(chatID, 'выбор', reply_markup=markup)



def listbuttons(list_buttons, row):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*list_buttons, row_width=row)
    return markup


@bot.message_handler(commands=['buttons2'])
def buttons2(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('1','2','3','4','5','6','7','8', row_width=4)


@bot.message_handler(commands=['привет', 'start'])
def send_welcome(message):
    chatID = message.from_user.id
    session[chatID] = {}
    list_buttons = '1','2','3'
    markup = listbuttons(list, 3)
    bot.send_message(message,'меню кнопок', reply_markup=markup)

@bot.message_handler(fync=lambda message: True)
def echo_message(message):
    text_message = message.text
    text_message = text_message.lower()
    if 'абоба' in text_message:
        bot.reply_to(message, 'абоба!!!')
    for symbol in text_message:
        bot.reply_to(message, symbol)

@bot.message_handler(commands=['random1'])
def message2(message):
    chat_ID = message.from_user.id
    bot_message = bot.send_dice(chat_ID, '⚽')
    print(bot_message.dice.value)

@bot.message_handler(commands=['sticker'])
def sticker(message):
    chat_ID = message.from_user.id
    bot.send_sticker(chat_ID, '⚽')

@bot.message_handler(commands=['doc'])
def doc(message):
    chat_ID = message.from_user.id
    bot.send_document(chat_ID, open('dfdfsdfdfsf.txt', 'rb'))

@bot.message_handler(commands=['photo'])
def photo(message):
    chat_ID = message.from_user.id
    bot.send_photo(chat_ID, 'https://s0.rbk.ru/v6_top_pics/media/img/5/31/756806793338315.png')

@bot.message_handler(commands=['gif'])
def gif(message):
    chat_id = message.from_user.id
    bot.send_photo(chat_id, open('nasa-black-hole-visualization-1.gif', 'rb'))



bot.infinity_polling()

