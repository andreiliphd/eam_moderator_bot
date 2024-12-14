import pprint
import redis
from flask import Flask, request, jsonify
import os
import time
import telebot
from dotenv import load_dotenv
from telebot.util import quick_markup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


load_dotenv()  # take environment variables from .env.

bot = telebot.TeleBot(os.getenv("API_TOKEN"))
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home(): 
    data = request.json
    r = redis.Redis(
    host=os.getenv("HOST"),
    port=6379,
    password=os.getenv("PASSWORD"),
    ssl=True
    )    
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
    r = redis.Redis(
    host=os.getenv("HOST"),
    port=6379,
    password=os.getenv("PASSWORD"),
    ssl=True
    )    
    r.set("internal_view", str(data))
    keys = r.keys('*')
    result = []
    tmp = {}
    values = r.mget(keys)
    for i in range(len(keys)):
        tmp = [telebot.types.InlineKeyboardButton({'text': values[i],'callback_data': keys[i]})]
        result.append(tmp)
    tmp = [telebot.types.InlineKeyboardButton({'text': "Удалить остальные", 'callback_data': 'delete_all'})]
    result.append(tmp)
    bot.send_message(chat_id = data['message']['chat']['id'], text = "Одобрите посты: ", reply_markup = result)
    r.get(data['update_id'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
