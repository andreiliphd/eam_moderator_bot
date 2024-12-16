import os
import logging
import uvicorn
from telegram import Bot
from fastapi import FastAPI, Request

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()
bot = Bot(token=os.getenv("TOKEN"))

@app.get("/")
async def root(request: Request):
    logger.log(logging.error, str(request.json))
    return {"message": "Hello from FastAPI!", "req": request.json}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
