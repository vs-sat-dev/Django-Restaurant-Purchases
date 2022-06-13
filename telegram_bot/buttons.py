from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram

import os, django
import sys
from pathlib import Path

from hundlers import manager, store_worker

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_purchases.settings')
django.setup()

from restaurant.models import Ingridient, TelegramNotification, StoreTask

def button(update, context):
    query = update.callback_query
    variant = query.data[:3]
    query.answer()
    
    if variant == 'yes':
        ingredient_id = int(query.data[3:])
        try:
            ingredient = Ingridient.objects.get(id=ingredient_id)
            context.user_data['ingredient_name'] = ingredient.name
            query.edit_message_text(text=f"How much {ingredient.name} must be bouth?:")
            context.bot_data['status'] = 'add_ingredient'
        except:
            query.edit_message_text(text=f"Ingredient does not exist")
    elif variant == 'not':
        ingredient_id = int(query.data[3:])
        try:
            ingredient = Ingridient.objects.get(id=ingredient_id)
            context.user_data['ingredient_name'] = ingredient.name
            query.edit_message_text(text="Ok")

            tn = TelegramNotification.objects.get(ingredient__id=ingredient.id)
            tn.delete()
        except:
            query.edit_message_text(text=f"Ingredient does not exist")
    elif variant == 'all':
        try:
            store_tasks = StoreTask.objects.all()
            if store_tasks is not None:
                for task in store_tasks:
                    text = f'You must buy {task.quantity} of {task.ingredient.name}'
                    keyboard = [
                        [
                            InlineKeyboardButton("I bouth it", callback_data=f'buy{task.ingredient.id}'),
                        ],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                    bot.sendMessage(chat_id=store_worker, text=text, reply_markup=reply_markup) 
            else:
                bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                bot.sendMessage(chat_id=store_worker, text=f'You haven\'t tasks') 
        except:
            bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
            bot.sendMessage(chat_id=store_worker, text=f'Some thing go wrong') 
    
    elif variant == 'rst':
        try:
            store_tasks = StoreTask.objects.all()
            if len(store_tasks) > 0:
                for task in store_tasks:
                    text = f'You required {task.quantity} of {task.ingredient.name}'
                    bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                    bot.sendMessage(chat_id=store_worker, text=text) 
            else:
                bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                bot.sendMessage(chat_id=manager, text=f'You haven\'t requirements') 
        except:
            bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
            bot.sendMessage(chat_id=store_worker, text=f'Some thing go wrong') 

    elif variant == 'buy':
        ingredient_id = int(query.data[3:])
        try:
            ingredient = Ingridient.objects.get(id=ingredient_id)
            try:
                store_task = StoreTask.objects.get(ingredient__id=ingredient_id)
                if store_task:
                    keyboard = [
                        [
                            InlineKeyboardButton("Look all your requirements", callback_data='rst'),
                        ],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                    bot.sendMessage(chat_id=manager, text=f'The store worker bouth {store_task.quantity} of {store_task.ingredient.name}',
                                    reply_markup=reply_markup) 
                    
                    ingredient.quantity = store_task.quantity
                    ingredient.save(update_fields=['quantity'])

                    store_task.delete()
                    tn = TelegramNotification.objects.get(ingredient__id=ingredient_id)
                    tn.delete()
                    query.edit_message_text(text="Ok")
                else:
                    bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                    bot.sendMessage(chat_id=store_worker, text=f'This StoreTask was not found') 
            except:
                bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
                bot.sendMessage(chat_id=store_worker, text=f'Some thing with StoreTask go wrong') 
        except:
            bot = telegram.Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
            bot.sendMessage(chat_id=store_worker, text=f'Some thing with ingredient go wrong') 

