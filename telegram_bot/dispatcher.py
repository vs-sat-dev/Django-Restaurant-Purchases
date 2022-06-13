import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes
import telegram

from buttons import button
from hundlers import callback_minute, start, custom_command, api_token


import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_purchases.settings')
django.setup()


from restaurant.models import Ingridient, TelegramNotification

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    updater = Updater(api_token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_command))

    jq = updater.job_queue
    job_minute = jq.run_repeating(callback_minute, interval=5)

    updater.start_polling()
    updater.idle()