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


def one_time():
    current_time = datetime.datetime.strftime(datetime.datetime.utcnow(),"%H")
    logging.debug('Current time is: ' + current_time)
    if current_time == "09":
        logging.debug('Sending scheduled messages')
        try:
            for brigadir in users.find({"position": "Айдос"}):
                cid = brigadir["user"]
                markup = types.ForceReply(selective=False)
                bot.send_message(cid, "ГКИБ: Количество проложенных труб в общем?", reply_markup=markup)
        except:
            bot.send_message(group_id, "Айдос не зарегался")
    
        try:
            cid = users.find_one({"position": "Снабжение"})["user"]
            markup = types.ForceReply(selective=False)
            bot.send_message(cid, "Какое количество произведенных станций в КНР сейчас?", reply_markup=markup)
        except:
            bot.send_message(group_id, "Анвар не зарегался")

        try:
            cid = users.find_one({"position": "Производство"})["user"]
            markup = types.ForceReply(selective=False)
            bot.send_message(cid, "Количество произведенных консолей на 1 газ в общем??", reply_markup=markup)
        except:
            bot.send_message(group_id, "Игорь Е. не зарегался")
        

if __name__ == "__main__":
    one_time()
    time.sleep(3600)
    