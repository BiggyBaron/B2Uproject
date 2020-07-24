#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2019"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

import telebot
from telebot import types
from pprint import pprint
import logging
from pymongo import MongoClient
import pymongo
import datetime
import time


client = MongoClient('mongodb://database:27017/')
db = client.b2u
users = db['users']
problems = db['problems']
msgs = db['messages']
dash = db['dash']


bot = telebot.TeleBot("806603779:AAGXStpRxg5Gks5o2nUKh_JOYziZObKXoCs")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
group_id = -1001438155243


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    hello_string = 'Пройдите регистрацию: укажите свой номер'
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
    keyboard.add(reg_button)

    user = {
        "user": str(message.chat.id),
        "tlgfirstname": str(message.chat.first_name),
        "tlglastname": str(message.chat.last_name),
        "tlgusername": str(message.chat.username),
        "registration": message.date,
        "phone": "",
        "object": "",
        "name": "",
        "surname": ""
        }
    users.insert_one(user)
    
    bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    if message.contact is not None:
        if users.count_documents({"user": str(message.chat.id)})>0:
            users.update_one({"user": str(message.chat.id)}, { "$set": { "phone": str(message.contact.phone_number)}})
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Введите фамилию и имя:", reply_markup=markup)
        else:
            user = {
            "user": str(message.chat.id),
            "tlgfirstname": str(message.chat.first_name),
            "tlglastname": str(message.chat.last_name),
            "tlgusername": str(message.chat.username),
            "registration": message.date,
            "phone": str(message.contact.phone_number)
            }
            users.insert_one(user)
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
    
    if message.text.split(" ")[0].lower() == "проблема":
        msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "message": message.text
            }
        problems.insert_one(msg)
        after_registration = "Ваша проблема была зарегестрирована, можете приложить фото"
        bot.send_message(message.chat.id, after_registration)
    else:
        msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "message": message.text
            }
        msgs.insert_one(msg)

    # region: Position
        if message.text.split(":")[0] == 'Позиция':
            if users.count_documents({"user": str(message.chat.id)})>0:
                users.update_one({"user": str(message.chat.id)}, { "$set": { "position": str(message.text.split(" ")[1])}})
                after_registration = "Теперь если есть проблема, то пишите сюда, с указанием объекта, причины и срочности. Срочность может быть от 1 до 9, где 1 - надо решать прям сейчас, а 9 - можно решить через 9 дней."
                bot.send_message(message.chat.id, after_registration)

                after_registration = "Пример сообщения:"
                bot.send_message(message.chat.id, after_registration)

                after_registration = "проблема 1 Больница №2 у нас закончились материалы"
                bot.send_message(message.chat.id, after_registration)

                after_registration = "Где проблема надо писать обязательно, 1 - срочность, знаки препинания не нужны"
                bot.send_message(message.chat.id, after_registration)

                after_registration = "Можно также приложить фото"
                bot.send_message(message.chat.id, after_registration)
            else:
                hello_string = 'Пройдите регистрацию: укажите свой номер'
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
                keyboard.add(reg_button)
                bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)
        # endregion
    
    # region: Replies
    if message.reply_to_message:

        # region: Name and surname
        if message.reply_to_message.text == 'Введите фамилию и имя:':
            if len(message.text.split(" ")) == 2:
                name = message.text.split(" ")[0]
                surname = message.text.split(" ")[1]
                
                if users.count_documents({"user": str(message.chat.id)})>0:
                    users.update_one({"user": str(message.chat.id)}, { "$set": { "name": str(name), "surname": str(surname)}})
                    after_registration = "Выберите Вашу позицию"
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row('Позиция: Снабжение')
                    markup.row('Позиция: Производство')
                    markup.row('Позиция: Бригадир')
                    markup.row('Позиция: Склад')
                    markup.row('Позиция: Другое')
                    bot.send_message(message.chat.id, after_registration, reply_markup=markup)
                else:
                    hello_string = 'Пройдите регистрацию: укажите свой номер'
                    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
                    keyboard.add(reg_button)
                    bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "Пример: Иванов Иван")
                bot.send_message(message.chat.id, "Введите фамилию и имя:", reply_markup=markup)
        # endregion

        # region: Checking data

        # region: production
        if message.reply_to_message.text == 'Количество произведенных консолей на 1 газ за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "p1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Количество произведенных консолей на 3 газа за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество произведенных консолей на 3 газа за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "p3"
            }
            dash.insert_one(msg)
        # endregion

        # region: mount
        if message.reply_to_message.text == 'Количество проложенных труб внутри здания за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде ғимараттың сыртында салынған трубалардын  саны?")
            bot.send_message(message.chat.id, "Количество проложенных труб снаружи здания за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество проложенных труб снаружи здания за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m2"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде 1 газға орнатылған (іске қосылмаған) консольдердің саны?")
            bot.send_message(message.chat.id, "Количество установленных (не запущенных) консолей на 1 газ за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество установленных (не запущенных) консолей на 1 газ за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m3"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде 3 газға орнатылған (іске қосылмаған) консольдердің саны?")
            bot.send_message(message.chat.id, "Количество установленных (не запущенных) консолей на 3 газа за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество установленных (не запущенных) консолей на 3 газа за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m4"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде 1 газға арналған консольдердің саны? ")
            bot.send_message(message.chat.id, "Количество запущенных консолей на 1 газ за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество запущенных консолей на 1 газ за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m5"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде 3 газға арналған консольдердің саны? ")
            bot.send_message(message.chat.id, "Количество запущенных консолей на 3 газа за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество запущенных консолей на 3 газа за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m6"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде жалпы мақсаттағы толық дайын палаталардың саны?")
            bot.send_message(message.chat.id, "Количество полностью готовых палат общего назначения за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество полностью готовых палат общего назначения за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m7"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде операциялық блоктың толық дайын палаталарының саны?")
            bot.send_message(message.chat.id, "Количество полностью готовых палат операционного блока за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество полностью готовых палат операционного блока за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m8"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Соңғы 24 сағат ішінде толық дайын реанимация палаталарының саны?")
            bot.send_message(message.chat.id, "Количество полностью готовых палат реанимации за последние 24 часа?", reply_markup=markup)
        if message.reply_to_message.text == 'Количество полностью готовых палат реанимации за последние 24 часа?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m9"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Сіз іске қосу-жөндеу жұмыстарын бастадыңыз ба? (+/-)")
            bot.send_message(message.chat.id, "Начали ли Вы пуско-наладочные работы? (+/-)", reply_markup=markup)
        if message.reply_to_message.text == 'Начали ли Вы пуско-наладочные работы? (+/-)':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m10"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Іске қосу-жөндеу жұмыстарын аяқтадыңыз ба? (+/-)")
            bot.send_message(message.chat.id, "Закончили ли Вы пуско-наладочные работы? (+/-)", reply_markup=markup)
        if message.reply_to_message.text == 'Закончили ли Вы пуско-наладочные работы? (+/-)':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m11"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Сіздің объектіңізде станция тұр ма? (+/-)")
            bot.send_message(message.chat.id, "Стоится ли станция у Вас на объекте? (+/-)", reply_markup=markup)
        if message.reply_to_message.text == 'Стоится ли станция у Вас на объекте? (+/-)':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m12"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Сіздің объектіде станция толығымен кұрылды ма? (+/-)")
            bot.send_message(message.chat.id, "Построена ли станция у Вас на объекте? (+/-)", reply_markup=markup)
        if message.reply_to_message.text == 'Построена ли станция у Вас на объекте? (+/-)':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "m13"
            }
            dash.insert_one(msg)
        # endregion
        
        # region: warehouse
        if message.reply_to_message.text == 'Какое количество центральных крышек на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество оснований на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество оснований на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w2"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество боковых оснований на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество боковых оснований на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w3"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество боковых крышек на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество боковых крышек на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w4"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество соединительных профилей на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество соединительных профилей на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w5"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество рельс на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество рельс на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w6"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество боковых крышек на двойные на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество боковых крышек на двойные на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w7"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество клапанов AIR на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество клапанов AIR на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w8"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество клапанов VAC на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество клапанов VAC на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w9"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество клапанов CO2 на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество клапанов CO2 на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w10"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество клапанов O2 на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество клапанов O2 на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w11"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество СИЗов на складе сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество СИЗов на складе сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "w12"
            }
            dash.insert_one(msg)
        # endregion
        
        # region: Anvar
        if message.reply_to_message.text == 'Какое количество произведенных станций на 20 м3 в КНР сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество произведенных станций на 30 м3 в КНР сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество произведенных станций на 30 м3 в КНР сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a2"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество произведенных станций на 50 м3 в КНР сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество произведенных станций на 50 м3 в КНР сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a3"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество доставленных в РК станций на 20 м3 сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество доставленных в РК станций на 20 м3 сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a4"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество доставленных в РК станций на 30 м3 сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество доставленных в РК станций на 30 м3 сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a5"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Какое количество доставленных в РК станций на 50 м3 сейчас?", reply_markup=markup)
        if message.reply_to_message.text == 'Какое количество доставленных в РК станций на 50 м3 сейчас?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "type": "a6"
            }
            dash.insert_one(msg)
            bot.send_message(message.chat.id, "Спасибо за Ваши ответы")
        # endregion
        
        # endregion
    
    # endregion


@bot.message_handler(content_types=['image'])
def text_handler2(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)



if __name__ == "__main__":
    bot.polling()