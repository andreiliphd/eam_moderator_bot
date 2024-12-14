import pprint
import redis
from flask import Flask, request, jsonify
import os
import time
import telebot
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

bot = telebot.TeleBot(os.getenv("API_TOKEN"))
app = Flask(__name__)
chat = ""

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
    r.set(data['update_id'], data['message']['from']['username'] + ' - ' + data['message']['text'])
    bot.delete_message(data['message']['chat']['id'], data['message']['message_id'])
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
    text = {"inline_keyboard": []}
    keys = r.keys('*')
    values = r.mget(keys)
    for i in range(len(keys)):
        tmp = text['inline_keyboard'].append([{'callback_data': keys[i], 'text': values[i]}])
    bot.send_message(chat_id = chat, reply_markup = text)
    r.get(data['update_id'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
