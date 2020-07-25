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


bot = telebot.TeleBot("806603779:AAGXStpRxg5Gks5o2nUKh_JOYziZObKXoCs")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
group_id = -1001438155243


names = [
    "398812967",
    "1128599181",
    "919315320",
    "1154083994",
    "467700430",
    "1162808560",
    "1290766437",
    "1327755449"
]


for user in names:
    markup = types.ForceReply(selective=False)
    text = 'Добрый день, коллеги!\n'\
    'Начиная с завтрашнего дня, отчет будет появляться в 10 часов утра, и обязателен для заполнения до 12 часов.\n'\
    'Обеды и ужины для бригад будут формироваться из списка тех, кто ответил на отчет.\n'\
    'Просим ответить на это сообщение любой фразой из "Принял, ок, да, хорошо, жарайды". Спасибо за внимание!\n'\
    'Всем хорошего дня!'
    bot.send_message(user, text, reply_markup=markup)

