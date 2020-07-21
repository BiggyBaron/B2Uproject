import telebot
from telebot import types
from pprint import pprint
import logging


bot = telebot.TeleBot("806603779:AAGXStpRxg5Gks5o2nUKh_JOYziZObKXoCs")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='allData.log',level=logging.DEBUG)
group_id = -1001438155243

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    hello_string = 'Пройдите регистрацию: укажите свой номер'
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
    keyboard.add(reg_button)

    bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    if message.contact is not None:
        print(message.contact)
        print(message.contact.phone_number)
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите фамилию и имя:", reply_markup=markup)
    else:
        hello_string = 'Регистрация обязательна'
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
        keyboard.add(reg_button)
        bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    
    # Replies
    if message.reply_to_message:

        # Name and surname
        if message.reply_to_message.text == 'Введите фамилию и имя:':
            if len(message.text.split(" ")) == 2:
                name = message.text.split(" ")[0]
                surname = message.text.split(" ")[1]
                print(name)
                print(surname)
                after_registration = "Выберите Вашу позицию"
                markup = types.ReplyKeyboardMarkup()
                markup.row('Директор снабжения')
                markup.row('Директор монтажа')
                markup.row('Директор производства')
                markup.row('Директор по строительству')
                markup.row('Директор по связи')
                markup.row('Тех. надзор')
                markup.row('Бригадир №1')
                markup.row('Бригадир №2')
                markup.row('Бригадир №3')
                markup.row('Бригадир №4')
                markup.row('Бригадир №5')
                markup.row('Бригадир №6')
                markup.row('Бригадир №7')
                markup.row('Бригадир №8')
                markup.row('Бригадир №9')
                markup.row('Бригадир №10')
                markup.row('Бригадир №11')
                markup.row('Бригадир №12')
                markup.row('Бригадир №13')
                markup.row('Бригадир №14')
                markup.row('Бригадир №15')
                markup.row('Бригадир №16')
                markup.row('Бригадир №17')
                markup.row('Бригадир №18')
                bot.send_message(message.chat.id, after_registration, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Пример: Иванов Иван")
                bot.send_message(message.chat.id, "Введите фамилию и имя:", reply_markup=markup)


@bot.message_handler(content_types=['image'])
def text_handler(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)


bot.polling()