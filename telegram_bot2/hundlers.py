import telegram
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

import os, django
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_purchases.settings')
django.setup()

from restaurant.models import Ingridient, TelegramNotification, StoreTask


api_token = '5101746704:AAFsx6e4if1K5LTfxr3vCUycH59jOR-aN7g'
allowed_users = ['241630970', '314722445']
manager = '241630970'
store_worker = '241630970'


def start(update, context):
    if str(update.message.from_user.id) in allowed_users:
        if update.message.from_user.id == manager:
            context.bot_data['status'] = 'idle'
        update.message.reply_text('Hello!')
    else:
        update.message.reply_text('Forbidden')

def custom_command(update: Update, context: ContextTypes) -> None:

    if str(update.message.from_user.id) in allowed_users:
        text = update.message.text
        if context.bot_data['status'] == 'add_ingredient' and str(update.message.from_user.id) == manager:
            try:
                text = float(update.message.text)
                context.bot_data['status'] = 'idle'
                ingredient = Ingridient.objects.get(name=context.user_data["ingredient_name"])
                StoreTask.objects.create(ingredient=ingredient, quantity=text)

                keyboard = [
                    [
                        InlineKeyboardButton("Look all tasks", callback_data='all'),
                        InlineKeyboardButton("I bouth it", callback_data=f'buy{ingredient.id}'),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                bot = telegram.Bot(token=api_token)
                bot.sendMessage(chat_id=store_worker, text=f'You must buy {text} {context.user_data["ingredient_name"]}. Do you want to look all your tasks?',
                                reply_markup=reply_markup)

                tn = TelegramNotification.objects.filter(status='busy_task').first()
                tn.status = 'process_task'
                tn.save(update_fields=['status'])
            except:
                text = 'Quantity must be numeric'
                update.message.reply_text(text)
    else:
        update.message.reply_text('Forbidden')

def callback_minute(context: telegram.ext.CallbackContext):

    try:
        context.bot_data['status']
    except:
        context.bot_data['status'] = 'idle'

    ingredient_status = TelegramNotification.objects.filter(status='busy_task')
    if len(ingredient_status) == 0:
        tn = TelegramNotification.objects.filter(status='free_task').first()
        if tn:
            ingredient = tn.ingredient

            context.bot_data['status'] = 'add_ingredient'

            tn.status = 'busy_task'
            tn.save(update_fields=['status'])
            keyboard = [
                [
                    InlineKeyboardButton("Yes", callback_data=f'yes{ingredient.id}'),
                    InlineKeyboardButton("No", callback_data=f'not{ingredient.id}'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot = telegram.Bot(token=api_token)
            bot.sendMessage(chat_id=manager, 
                text=f'The {ingredient.name} was ended. Quantity={ingredient.quantity}. Do you wish to buy it?', 
                reply_markup=reply_markup)
