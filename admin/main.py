#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template, request, Markup, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
import time
import random
from random import sample
import datetime
import socket
import json
from pymongo import MongoClient
import requests
from requests import Request, Session
from threading import Lock


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
app.config['JSON_AS_ASCII'] = False

client = MongoClient('mongodb://database:27017/')
db = client.b2u
users = db['users']
problems = db['problems']
msgs = db['messages']
dash = db['dash']
needs = db['needs']
data_now = db['data_now']
sklad = db["sklad"]

# Main page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html", **locals())


@socketio.on('connect', namespace='/test')
def test_connect():

    snabjenies = users.find_one({"position": "Снабжение"})
    sklads = users.find_one({"position": "Склад"})
    productions = users.find_one({"position": "Производство"})
    brigadirs = users.find_one({"position": "Бригадир"})

    senddata = data_now.find_one()

    senddata["_id"] = 0

    emit('my response', senddata)
   

# Main flask app
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)