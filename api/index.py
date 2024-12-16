import os
import logging
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def telegram_url_builder(method, **kwargs)  
    basic = "https://api.telegram.org/bot" + os.getenv("TOKEN") + "/" + str(method) + "?"
    for k, val in kwargs.items():
        print("%s == %s" % (k, val))
        basic += k + "=" + val + "&"
    basic = basic[-1]
    logger.log(logging.WARNING, str(basic)) 
    return basic


@app.route("/", methods = ["GET", "POST"])
def entry():
    data = request.json
    logger.log(logging.WARNING, str(data))
    return str(request.json)
