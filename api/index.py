import pprint
from flask import Flask, request, jsonify


class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app
    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)
        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)
        return self._app(env, log_response)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = request.json
    return jsonify(data)

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host='0.0.0.0', port=80)
