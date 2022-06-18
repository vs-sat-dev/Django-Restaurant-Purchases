import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes
import telegram

from buttons import button
from hundlers import callback_minute, start, custom_command, api_token

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_purchases.settings')
django.setup()

for fls in os.listdir():
    print('File: ', fls)
    f = open(fls, 'rb')
    print('content:\n', f.read())
    break

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

    tns = TelegramNotification.objects.all()
    for tn in tns:
        tn.delete()

    jq = updater.job_queue
    job_minute = jq.run_repeating(callback_minute, interval=5)

    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                       port=5000,
                       url_path=api_token, cert='fullchain.pem', key='privkey.pem',
                       webhook_url=f'https://chupakabra.monster/{api_token}')
    #updater.bot.setWebhook(f'https://chupakabra.monster/{api_token}', certificate=open('fullchain.pem', 'rb'))
    #updater.bot.setWebhook(f'https://134.122.43.197:8443/{api_token}')

    #updater.start_webhook(listen='0.0.0.0', port=8443, url_path='TOKEN',
    #                      key='private.key', cert='cert.pem',
    #                      webhook_url=f'https://134.122.43.197:8443/{api_token}')

    updater.idle()

