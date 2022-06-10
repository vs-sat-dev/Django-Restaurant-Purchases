import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes
import telegram

from buttons import button


import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_purchases.settings')
django.setup()


from restaurant.models import Ingridient, TelegramNotification

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


api_token = '5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw'
status = 'idle'
allowed_users = ['241630970']
manager = '241630970'
store_worker = '241630970'


def start(update, context):
    print('US: ', update.message.from_user)
    if str(update.message.from_user.id) in allowed_users:
        update.message.reply_text('Hello!')
    else:
        update.message.reply_text('Forbidden')

def custom_command(update: Update, context: ContextTypes) -> None:
    if str(update.message.from_user.id) in allowed_users:
        text = update.message.text
        global status
        if status == 'add_ingredient':
            try:
                text = float(update.message.text)
                status = 'idle'
                bot = telegram.Bot(token=api_token)
                bot.sendMessage(chat_id=store_worker, text=f'You must buy {text} {context.user_data["ingredient_name"]}')

                tn = TelegramNotification.objects.filter(status=1).first()
                tn.status = 2
                tn.save(update_fields=['status'])
            except:
                text = 'Quantity must be numeric'
                update.message.reply_text(text)
    else:
        update.message.reply_text('Forbidden')

def callback_minute(context: telegram.ext.CallbackContext):
    ingredient_status = TelegramNotification.objects.filter(status=1)
    print('step1 ', len(ingredient_status))
    if len(ingredient_status) == 0:
        print('step2')
        tn = TelegramNotification.objects.filter(status=0).first()
        if tn:
            print('step3')
            ingredient = tn.ingredient

            tn.status = 1
            tn.save(update_fields=['status'])
            keyboard = [
                [
                    InlineKeyboardButton("Yes", callback_data=f'yes{ingredient.id}'),
                    InlineKeyboardButton("No", callback_data=f'not{ingredient.id}'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
            bot.sendMessage(chat_id='241630970', 
                text=f'The {ingredient.name} was ended. Quantity={ingredient.quantity}. Do you wish buy it?', 
                reply_markup=reply_markup)

def help_command(update, _):
    update.message.reply_text("Используйте `/start` для тестирования.")

if __name__ == '__main__':
    # Передайте токен вашего бота.
    updater = Updater(api_token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_command))

    jq = updater.job_queue
    job_minute = jq.run_repeating(callback_minute, interval=5)

    # Запуск бота
    updater.start_polling()
    updater.idle()