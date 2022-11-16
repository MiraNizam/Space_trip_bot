import telegram
from environs import Env

env = Env()
env.read_env()

bot = telegram.Bot(env.str("TG_TOKEN"))
bot.send_message(text="Hi, I'm space!", chat_id="@space_trip_channel")