import os
import logging
from sanic import Sanic
from sanic.response import text

app = Sanic("eam_moderator")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


@app.get("/")
async def hello_world(request):
    logger.log(logging.WARNING, str(request))
    return text("Hello, world.")
