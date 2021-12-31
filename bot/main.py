import telebot

from utils.config import TOKEN
from commands.timetable import timetable

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Все','Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'help')
    bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def rasp(message):
    if (message.text.split()[0] in ["Все",'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']):
        rasp = timetable(message=message.text)
        bot.send_message(message.chat.id, rasp)

    elif (message.text.split()[0] == 'help'):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Все",'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб')
        text = """
        Выберите день в списке комманд, чтобы увидеть расписание
        """
        bot.send_message(message.chat.id, text, reply_markup=keyboard)


bot.infinity_polling()