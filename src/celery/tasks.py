from celery import Celery
from celery.contrib.abortable import AbortableTask
from environs import Env

from src.utils.client_manipulator import BotHandler

env = Env()
env.read_env()

TEL_CLIENT_BOT_TOKEN = env.str("TEL_CLIENT_BOT_TOKEN")
REDIS_HOST = env.str("REDIS_HOST")
RABBITMQ_HOST = env.str("RABBITMQ_HOST")

bot_handler = BotHandler(TEL_CLIENT_BOT_TOKEN)

app = Celery("tasks", broker=f"amqp://{RABBITMQ_HOST}", backend=f"redis://{REDIS_HOST}")


def save_image():
    print("Image Saved!")


@app.task(bind=True, base=AbortableTask)
def breast_cancer_detection(self, chat_id):
    save_image()

    message = "Process finished!"
    if not self.is_aborted():
        resp = bot_handler.send_message(chat_id, message)
        print(resp.text)
