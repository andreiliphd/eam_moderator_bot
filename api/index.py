import pprint
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = request.json
    return jsonify(data)

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
