from dotenv import load_dotenv
from gpiozero import Servo
import logging
import os
from slack_bolt import App

load_dotenv(".env")

logging.basicConfig(level=logging.DEBUG)

servo = Servo(17)

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.event("message")
def strike_gong(client, event, body, logger, payload):
    print("reveiving message event...")
    try:
        logger.info(payload)

        if "Deal name: " in payload["text"]:
            Servo.mid()
            Servo.min()

    except Exception as e:
        logger.error(f"Error reading message: {e}")


@app.error
def global_error_handler(error, body, logger):
    logger.exception(error)
    logger.info(body)


if __name__ == "__main__":
    app.start(3000)
