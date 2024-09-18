from telegram import Bot
from bread_fast_bot.settings import get_settings

settings = get_settings()
bot = Bot(token=settings.token)
chat_id = 288438352

text = 'Вам телеграмма!'

bot.send_message(chat_id, text)
