import pprint
import redis
from flask import Flask, request, jsonify
import os
import time


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home(): 
    r = redis.Redis(
    host=os.getenv("HOST"),
    port=6379,
    password=os.getenv("PASSWORD"),
    ssl=True
    )    
    r.set(time.time(), str(request.json))
    data = request.json
    return jsonify(data)

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
