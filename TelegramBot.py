import threading
import requests
import telebot

bot = telebot.TeleBot('1160196994:AAHlGmduTo4skEko734VXINswaohZMRXYhM')

LastUserMessage = None


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Done')


@bot.message_handler(content_types=['text'])
def send_text(message):
    global LastUserMessage
    LastUserMessage = message
    print(message.chat.id)
    send_post_request(message.text)
    bot.send_message(message.chat.id, 'Done')


def reply_user(text):
    global LastUserMessage
    bot.send_message(LastUserMessage.chat.id, text)


def send_post_request(text):
    url = "http://localhost:8082/get/message"
    data = text

    r = requests.post(url=url, data=data.encode('utf-8'))
    pastebin_url = r.text

    print("The pastebin URL is:%s" % pastebin_url)


def start_bot():
    bot.polling()


def start():
    name = "telegram_bot"
    t = threading.Thread(target=start_bot, name=name)
    t.daemon = True
    t.start()
    print("Bot started")
