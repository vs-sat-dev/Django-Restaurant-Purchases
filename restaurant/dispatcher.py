import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


status = 'idle'


def start(update, _):
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Do you wish add ingredient?:', reply_markup=reply_markup)

async def custom_command(update: Update, context: ContextTypes) -> None:
    text = update.message.text
    if status == 'add_ingredient':
        try:
            text = float(update.message.text)
        except:
            text = 'Quantity must be numeric'
    await update.message.reply_text(text)


def button(update, _):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если 
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы. 
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    # редактируем сообщение, тем самым кнопки 
    # в чате заменятся на этот ответ.
    if variant == 'yes':
        status = 'add_ingredient'
        query.edit_message_text(text=f"How much ingredient must be bouth?")

def help_command(update, _):
    update.message.reply_text("Используйте `/start` для тестирования.")

if __name__ == '__main__':
    # Передайте токен вашего бота.
    updater = Updater("5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()