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
import pymongo
import requests
from requests import Request, Session
from threading import Lock
import logging


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

logging.basicConfig(level=logging.WARNING)


def calculate():

    objects = dash.distinct("object")
    types = dash.distinct("type")

    consoles1 = dash.find_one({"type": "p1"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    consoles3 = dash.find_one({"type": "p2"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    rsh = dash.find_one({"type": "p3"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    krb = dash.find_one({"type": "p4"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    comp_station = dash.find_one({"type": "p5"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    vac_station = dash.find_one({"type": "p6"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    oxy_station = dash.find_one({"type": "p7"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    
    prod_oxy = dash.find_one({"type": "a1"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    delv_oxy = dash.find_one({"type": "a2"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    prod_vac = dash.find_one({"type": "a3"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    delv_vac = dash.find_one({"type": "a4"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    prod_comp = dash.find_one({"type": "a5"}, sort=[( '_id', pymongo.DESCENDING )])["data"]
    delv_comp = dash.find_one({"type": "a6"}, sort=[( '_id', pymongo.DESCENDING )])["data"]

    obj_data = {"total": {"tubes": 0, "krb": 0, "rsh": 0, "cons1": 0, "cons3": 0, "vac": 0, "comp": 0, "oxy": 0}}
    needed_data = {"total": {"tubes": 0, "krb": 0, "rsh": 0, "cons1": 0, "cons3": 0, "vac": 0, "comp": 0, "oxy": 0}}

    for obj in objects:
        obj_data[obj] = {}
        needed_data[obj] = {}

        obj_data[obj]["tubes"] = dash.find_one({"type": "m1", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["tubes"] = obj_data["total"]["tubes"] + int(obj_data[obj]["tubes"])
        needed_data[obj]["tubes"] = needs.find_one({"object": obj})["m1"]
        needed_data["total"]["tubes"] = needed_data["total"]["tubes"] + needs.find_one({"object": obj})["m1"]

        obj_data[obj]["krb"] = dash.find_one({"type": "m2", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["krb"] = obj_data["total"]["krb"] + int(obj_data[obj]["krb"])
        needed_data[obj]["krb"] = needs.find_one({"object": obj})["m2"]
        needed_data["total"]["krb"] = needed_data["total"]["krb"] + needs.find_one({"object": obj})["m2"]

        obj_data[obj]["rsh"] = dash.find_one({"type": "m3", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["rsh"] = obj_data["total"]["rsh"] + int(obj_data[obj]["rsh"])
        needed_data[obj]["rsh"] = needs.find_one({"object": obj})["m3"]
        needed_data["total"]["rsh"] = needed_data["total"]["rsh"] + needs.find_one({"object": obj})["m3"]

        obj_data[obj]["cons1"] = dash.find_one({"type": "m4", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["cons1"] = obj_data["total"]["cons1"] + int(obj_data[obj]["cons1"])
        needed_data[obj]["cons1"] = needs.find_one({"object": obj})["m4"]
        needed_data["total"]["cons1"] = needed_data["total"]["cons1"] + needs.find_one({"object": obj})["m4"]

        obj_data[obj]["cons3"] = dash.find_one({"type": "m5", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["cons3"] = obj_data["total"]["cons3"] + int(obj_data[obj]["cons3"])
        needed_data[obj]["cons5"] = needs.find_one({"object": obj})["m5"]
        needed_data["total"]["cons5"] = needed_data["total"]["cons3"] + needs.find_one({"object": obj})["m5"]
        
        obj_data[obj]["vac"] = dash.find_one({"type": "m6", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["vac"] = obj_data["total"]["vac"] + int(obj_data[obj]["vac"])
        needed_data[obj]["vac"] = needs.find_one({"object": obj})["m6"]
        needed_data["total"]["vac"] = needed_data["total"]["vac"] + needs.find_one({"object": obj})["m6"]

        obj_data[obj]["comp"] = dash.find_one({"type": "m7", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["comp"] = obj_data["total"]["comp"] + int(obj_data[obj]["comp"])
        needed_data[obj]["comp"] = needs.find_one({"object": obj})["m7"]
        needed_data["total"]["comp"] = needed_data["total"]["comp"] + needs.find_one({"object": obj})["m7"]

        obj_data[obj]["oxy"] = dash.find_one({"type": "m8", "object": str(obj)}, sort=[( '_id', pymongo.DESCENDING )])["data"]
        obj_data["total"]["oxy"] = obj_data["total"]["oxy"] + int(obj_data[obj]["oxy"])
        needed_data[obj]["oxy"] = needs.find_one({"object": obj})["m8"]
        needed_data["total"]["oxy"] = needed_data["total"]["oxy"] + needs.find_one({"object": obj})["m8"]

    logging.warning(needed_data)




# Main page
@app.route("/", methods=["GET", "POST"])
def index():
    # calculate()
    return render_template(
        "index.html", **locals())


# Main page
@app.route("/test/", methods=["GET", "POST"])
def index2():
    calculate()
    return render_template(
        "index.html", **locals())


@socketio.on('connect', namespace='/test')
def test_connect():
    senddata = data_now.find_one()
    senddata["_id"] = 0
    emit('my response', senddata)


@app.route("/enter", methods=["GET", "POST"])
def enter():
    return render_template(
        "enter.html", **locals())


# Main flask app
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)