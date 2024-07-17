import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
from random import  randint
import os

session = {}
load_dotenv(find_dotenv())
token = os.getenv('token')

bot = telebot.TeleBot(token)

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


@bot.message_handler(commands=['buttons'])
def buttons(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('1','2','3','4','5','6','7','8', row_width=4)
    bot.send_message(chatID, 'эмоция сигмы', reply_markup=markup)


@bot.message_handler(commands=['привет', 'start'])
def send_welcome(message):
    chatid = message.from_user.id
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

@bot.message_handler(commands=['game'])
def game(message):
    bot.send_game()



bot.infinity_polling()

