import telebot

token = '7071800191:AAGIs28xt9bsQonvemOezuxjG0K1M9U9nGI'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['привет', 'start'])
def send_welcome(message):
    name = message.from_user.username
    print(name)
    bot.reply_to(message,'привет',name)


@bot.message_handler(fync=lambda message: True)
def echo_message(message):
    text_message = message.text
    text_message = text_message.lower()
    if 'абоба' in text_message:
        bot.reply_to(message, 'абоба!!!')
    for symbol in text_message:
        bot.reply_to(message, symbol)

t.me/+SMh9YT_AOnl4MjQ6

bot.infinity_polling()

