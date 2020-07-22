#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2019, Buyqaw LLP"
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


client = MongoClient('mongodb://database:27017/')
db = client.b2u
users = db['users']


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

    user = {
        "user": str(message.chat.id),
        "tlgfirstname": str(message.chat.first_name),
        "tlglastname": str(message.chat.last_name),
        "tlgusername": str(message.chat.username),
        "registration": message.chat.date
        }
    users.insert_one(user)
    
    bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)
    if message.contact is not None:
        if users.count_documents({"user": message.chat.id})>0:
            users.update_one({"user": message.chat.id}, { "$set": { "phone": str(message.contact.phone_number)}})
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "Введите фамилию и имя:", reply_markup=markup)
        else:
            user = {
            "user": str(message.chat.id),
            "tlgfirstname": str(message.chat.first_name),
            "tlglastname": str(message.chat.last_name),
            "tlgusername": str(message.chat.username),
            "registration": message.chat.date,
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
    
    # Replies
    if message.reply_to_message:

        # Name and surname
        if message.reply_to_message.text == 'Введите фамилию и имя:':
            if len(message.text.split(" ")) == 2:
                name = message.text.split(" ")[0]
                surname = message.text.split(" ")[1]
                
                if users.count_documents({"user": message.chat.id})>0:
                    users.update_one({"user": message.chat.id}, { "$set": { "name": str(name), "surname": str(surname)}})
                    after_registration = "Выберите Вашу позицию"
                    markup = types.ReplyKeyboardMarkup()
                    markup.row('Склад')
                    markup.row('Директор производства')
                    markup.row('Бригадир №1')
                    markup.row('Бригадир №2')
                    markup.row('Бригадир №3')
                    markup.row('Бригадир №4')
                    markup.row('Бригадир №5')
                    markup.row('Бригадир №6')
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

        # Postion
        if message.reply_to_message.text == 'Выберите Вашу позицию':
            


@bot.message_handler(content_types=['image'])
def text_handler2(message):
    bot.forward_message(group_id, message.chat.id, message.message_id)


bot.polling()