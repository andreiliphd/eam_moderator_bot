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

@app.route("/", methods = ["GET", "POST"])
def entry():
    data = request.json
    logger.log(logging.WARNING, str(data))
    return str(request.json)
