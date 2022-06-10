from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token='5281891159:AAHq0q3fFn-b0oNyM5SAqIaPeXsBrwueSyw')
dispatcher = Dispatcher(bot)

button = InlineKeyboardButton('Add Ingredient', callback_data='add')
markup = InlineKeyboardMarkup()
markup.add(button)


@dispatcher.message_handler(commands=['start', 'help'])
async def start(message: Message):
    await message.reply('Hello Telegram!', reply_markup=markup)

@dispatcher.message_handler(commands='add_ingredient')
async def add(message: Message):
    await message.reply('add_ingredient', reply_markup=markup)


executor.start_polling(dispatcher, skip_updates=True)
