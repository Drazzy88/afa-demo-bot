import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yookassa

# Токен Telegram бота
TOKEN = '7273007218:AAGEu9pfp316lSdbB4cNyhNjb3GKEWA8--M'

# Идентификатор Google Calendar
CALENDAR_ID = '81dd85e0cc96f5cb5ebeafbfe182e6c07c57f9c3e2b6bf67dfdbbc80848c1064@group.calendar.google.com'

# Данные YooKassa
SHOP_ID = '506751'
SHOP_ARTICLE_ID = '538350'
YOOKASSA_TOKEN = '381764678:TEST:87458'

logging.basicConfig(level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот для приема на онлайн курсы.')

def register(update, context):
    # Создаем форму заявки
    keyboard = [
        [{'text': 'Заполнить форму'}]
    ]
    reply_markup = {'keyboard': keyboard, 'resize_keyboard': True}
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заполните форму заявки:', reply_markup=reply_markup)

def form(update, context):
    # Обработка формы заявки
    text = update.message.text
    if text == 'Заполнить форму':
        # Создаем форму заявки
        keyboard = [
            [{'text': 'Имя и Фамилия'}],
            [{'text': 'Номер мобильного телефона'}],
            [{'text': 'Выбрать дату и время'}]
        ]
        reply_markup = {'keyboard': keyboard, 'resize_keyboard': True}
        context.bot.send_message(chat_id=update.effective_chat.id, text='Заполните форму заявки:', reply_markup=reply_markup)
    elif text.startswith('Имя и Фамилия'):
        # Обработка имени и фамилии
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите имя и фамилию:')
    elif text.startswith('Номер мобильного телефона'):
        # Обработка номера мобильного телефона
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите номер мобильного телефона:')
    elif text.startswith('Выбрать дату и время'):
        # Обработка даты и времени
        # Создаем календарь через API Google Calendar
        creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/calendar'])
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': 'Онлайн курс',
            'location': 'Онлайн',
            'description': 'Онлайн курс',
            'start': {
                'dateTime': '2023-03-01T09:00:00',
                'timeZone': 'Europe/Moscow'
            },
            'end': {
                'dateTime': '2023-03-01T10:00:00',
                'timeZone': 'Europe/Moscow'
            },
            'attendees': [
                {'email': 'user@example.com'}
            ]
        }
        try:
            event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        except HttpError as error:
            print('An error occurred: %s' % error)

def payment(update, context):
    # Обработка оплаты
    keyboard = [
        [{'text': 'Серебро 2000 рублей'}],
        [{'text': 'Золото 3000 рублей'}],
        [{'text': 'Платина 4000 рублей'}]
    ]
    reply_markup = {'keyboard': keyboard, 'resize_keyboard': True}
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите тариф:', reply_markup=reply_markup)

def process_payment(update, context):
    # Обработка оплаты через YooKassa
    text = update.message.text
    if text == 'Серебро 2000 рублей':
        amount = 2000
    elif text == 'Золото 3000 рублей':
        amount = 3000
    elif text == 'Платина 4000 рублей':
        amount = 4000
    yookassa_token = YOOKASSA_TOKEN
    shop_id = SHOP_ID
    shop_article_id = SHOP_ARTICLE_ID
    payment_id = yookassa.Payment.create({
        'amount': amount,
        'currency': 'RUB',
        'payment_method_types': ['bank_card'],
        'confirmation': {
            'type': 'edirect',
            'eturn_url': 'https://example.com'
        }
    })
    context.bot.send_message(chat_id=update.effective_chat.id, text='Оплата прошла успешно!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('register', register))
    dp.add_handler(MessageHandler(Filters.text, form))
    dp.add_handler(MessageHandler(Filters.text, process_payment))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
