from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from restaurant.models import Ingridient, TelegramNotification


def button(update, context):
    query = update.callback_query
    variant = query.data[:3]

    print('QData: ', query.data)

    # `CallbackQueries` требует ответа, даже если 
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы. 
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    global status
    # редактируем сообщение, тем самым кнопки 
    # в чате заменятся на этот ответ.
    if variant == 'yes':
        ingredient_id = int(query.data[3:])
        status = 'add_ingredient'
        try:
            ingredient = Ingridient.objects.get(id=ingredient_id)
            context.user_data['ingredient_name'] = ingredient.name
            query.edit_message_text(text=f"How much {ingredient.name} must be bouth?:")
        except:
            status = 'idle'
            query.edit_message_text(text=f"Ingredient does not exist")
    elif variant == 'not':
        ingredient_id = int(query.data[3:])
        try:
            print('del1')
            ingredient = Ingridient.objects.get(id=ingredient_id)
            print('del2')
            context.user_data['ingredient_name'] = ingredient.name
            print('del3')
            query.edit_message_text(text="Ok")
            print('del4')

            tn = TelegramNotification.objects.get(ingredient__id=ingredient.id)
            print('del5')
            tn.delete()
            print('del6')
        except:
            status = 'idle'
            query.edit_message_text(text=f"Ingredient does not exist")
