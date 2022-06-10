import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes
import telegram

from restaurant.models import Ingridient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


api_token = '5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw'
status = 'idle'
allowed_users = ['241630970']
manager = '241630970'
store_worker = '241630970'


def start(update, _):
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
                bot.sendMessage(chat_id=store_worker, text=f'You must buy {text}')
            except:
                text = 'Quantity must be numeric'
                update.message.reply_text(text)
    else:
        update.message.reply_text('Forbidden')


def button(update, _):
    query = update.callback_query
    variant = query.data[:3]

    print('QData: ', query.data)

    # `CallbackQueries` требует ответа, даже если 
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы. 
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    # редактируем сообщение, тем самым кнопки 
    # в чате заменятся на этот ответ.
    if variant == 'yes':
        ingredient_id = int(query.data[3:])
        global status
        status = 'add_ingredient'
        query.edit_message_text(text=f"How much ingredient must be bouth?:")

def help_command(update, _):
    update.message.reply_text("Используйте `/start` для тестирования.")

if __name__ == '__main__':
    # Передайте токен вашего бота.
    updater = Updater(api_token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()