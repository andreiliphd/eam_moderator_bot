import pprint
import redis
import json
from flask import Flask, request, jsonify
import os
import time
import telebot
from dotenv import load_dotenv
from telebot.util import quick_markup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

bot = telebot.TeleBot(os.getenv("API_TOKEN"))
bot_2 = telebot.TeleBot(os.getenv("API_TOKEN_2"))

r = redis.Redis(
host=os.getenv("HOST"),
port=6379,
password=os.getenv("PASSWORD"),
ssl=True
)    

@app.route('/', methods=['GET', 'POST'])
def home(): 
    data = request.json
    chat = data['message']['chat']['id']
    try:
        r.set(data['update_id'], data['message']['from']['username'] + ' - ' + data['message']['text'])
    except KeyError:
        pass
    bot.delete_message(chat, data['message']['message_id'])
    return jsonify(data)

@app.route('/manage', methods=['GET', 'POST'])
def do():
    data = request.json
    keys = r.keys('*')
    values = r.mget(keys)
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(len(keys)):
        btn_my_site= telebot.types.InlineKeyboardButton(text=values[i], callback_data=keys[i])
        markup.add(btn_my_site)
    bot_2.send_message(chat_id = data['message']['chat']['id'], text = "Одобрите посты: ", reply_markup = markup)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
