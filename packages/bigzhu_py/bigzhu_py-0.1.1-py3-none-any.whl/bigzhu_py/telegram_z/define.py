import telebot
from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists
TEL_TOKEN = env('TEL_TOKEN')
CHAT_ID = env('CHAT_ID')
bot = telebot.TeleBot(
    TEL_TOKEN, parse_mode=None
)
