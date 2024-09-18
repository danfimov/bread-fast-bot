import logging

import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ExtBot, Filters, MessageHandler, Updater

from bread_fast_bot.settings import get_settings


settings = get_settings()
kitchen_chat_id = ""


menu_url = 'https://practicumgrade.github.io/course-material/bakery-menu.json'
logger = logging.getLogger(__name__)


def get_menu():
    try:
        response = requests.get(menu_url)
        response_json = response.json()
    except requests.exceptions.ConnectionError as error:
        logger.error(error)
        response_json = {'positions': []}
    names = []
    for position in response_json['positions']:
        names.append(position['name'])
    menu_prefix = 'Сегодня в меню: '
    menu_names = ', '.join(names)
    menu = menu_prefix + menu_names
    return menu


def show_menu(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, get_menu())


def process_order(update, context):
    chat = update.effective_chat
    if update.message.text.startswith('Закажи'):
        order_message_prefix = 'Новый заказ: '
        context.bot.send_message(
            chat_id=kitchen_chat_id,
            text=order_message_prefix + update.message.text,
        )
        context.bot.send_message(
            chat_id=chat.id,
            text='Передали сообщение на кухню, приходите завтра за заказом в любое время!'
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text='Начните сообщение с «Закажи», чтобы передать заказ на кухню.'
        )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/menu']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Добро пожаловать, {}.'.format(name),
        reply_markup=button
    )

    context.bot.send_message(chat.id, get_menu())
    context.bot.send_message(
        chat_id=chat.id,
        text='Начните сообщение с «Закажи», чтобы передать заказ на кухню.'
    )


if __name__ == '__main__':
    bot = ExtBot(token=settings.token)
    updater = Updater(bot=bot)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('menu', show_menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, process_order))

    updater.start_polling()
    updater.idle()
