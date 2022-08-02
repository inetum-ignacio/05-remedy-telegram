import os
import telebot
from dotenv import load_dotenv

load_dotenv()
ID_CHAT = os.getenv('ID_CHAT')
TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
bot = telebot.TeleBot(TOKEN_TELEGRAM)


def ChatTelegram(text):
    chat_id = ID_CHAT
    return bot.send_message(chat_id, text)


if __name__ == '__main__':
    ChatTelegram()
