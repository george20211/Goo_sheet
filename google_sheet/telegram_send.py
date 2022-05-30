from telegram import Bot
import os

class SenderMessages:

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    bot = Bot(token=TELEGRAM_TOKEN)

    def sended_message(message, user=None):
        send = SenderMessages
        try:
            send.bot.send_message(chat_id=user, text=message)
        except Exception:
            send.bot.send_message(chat_id=send.CHAT_ID, text='Ошибка в id юзера')