import telebot

token = '7431236563:AAFtcP2OSZ1MGXHuc6VgugrU-Apuejq8Pzk'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['привет', 'start'])
def send_welcome(message):
    name = message.from_user.username
    print(name)
    bot.send_message(message,'привет')

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

