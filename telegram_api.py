import telegram
from environs import Env
from telegram import InputMediaPhoto

env = Env()
env.read_env()

bot = telegram.Bot(env.str("TG_TOKEN"))
bot.send_document(chat_id="@space_trip_channel", document=open("images/nasa_apod_photos/2.jpg", "rb"))