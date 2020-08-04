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
from flask_basicauth import BasicAuth


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
app.config['JSON_AS_ASCII'] = False

app.config['BASIC_AUTH_USERNAME'] = 'b2u'
app.config['BASIC_AUTH_PASSWORD'] = 'kzb2uRK'

basic_auth = BasicAuth(app)

client = MongoClient('mongodb://database:27017/')
db = client.b2u
users = db['users']
problems = db['problems']
msgs = db['messages']
dash = db['dash']
needs = db['needs']
data_now_db = db['data_now']
sklad = db["sklad"]

logging.basicConfig(level=logging.WARNING)


def tubes_calc():

    objects = dash.distinct("object")
    new_tubes = {"total": {"values":[], "average": 0, "needed": 0}}

    for obj in objects:

        new_data = dash.find({'type': 'm1', 'object':obj}, sort=[( '_id', pymongo.DESCENDING )])
        new_dates = []
        new_values = []
        values = []
        times = []

        for date in new_data:
            time = datetime.datetime.fromtimestamp(date["time"]).strftime("%d.%m.%y")
            if not new_dates:
                if date["data"]!="0":
                    new_dates.append(time)
                    new_values.append(date["data"])
                    times.append(date["time"])
                    # values.append([new_dates[-1], (int(new_values[-1]))])
            else:
                if new_dates[-1]!=time and date["data"]!="0":
                    new_dates.append(time)
                    new_values.append(date["data"])
                    times.append(date["time"])
                    # values.append([new_dates[-1], (int(new_values[-1])-int(new_values[-2]))])
        
        new_values = new_values[::-1]
        times = times[::-1]
        new_dates = new_dates[::-1]

        for i in range(len(new_values)):
            if i>0:
                values.append([ datetime.datetime.timestamp(datetime.datetime.strptime(new_dates[i]*1000, "%d.%m.%y")) , int(new_values[i]) - int(new_values[i-1])])
            else:
                values.append([ datetime.datetime.timestamp(datetime.datetime.strptime(new_dates[i]*1000, "%d.%m.%y")) , int(new_values[i])])
        
        period = datetime.datetime.fromtimestamp(times[-1]) - datetime.datetime(2020, 7, 28, 0, 0, 0)
        average = round(float(new_values[-1])/period.days)
        need1 = needs.find_one({"object": obj})["m1"]
        period2 = 22
        needed = round(float(need1)/period2)

        # logging.warning("Объект: " + str(obj) + ", скорость сейчас: " + str(average) + ", а надо: " + str(needed))
        # logging.warning(values)
        # logging.warning(average)
        # logging.warning(needed)

        new_tubes[obj] = {"values": values, "average": average, "needed": needed}
        new_tubes["total"]["average"] = new_tubes["total"]["average"] + new_tubes[obj]["average"]
        new_tubes["total"]["needed"] = new_tubes["total"]["needed"] + new_tubes[obj]["needed"]
        
    last_day = new_data = datetime.datetime.strptime(datetime.datetime.fromtimestamp(dash.find_one({'type': 'm1', 'object':obj}, sort=[( '_id', pymongo.DESCENDING )])["time"]).strftime("%d.%m.%y"), "%d.%m.%y")
    all_days = (last_day - datetime.datetime(2020, 7, 28, 0, 0, 0)).days

    for i in range(all_days):
        today = datetime.datetime(2020, 7, 28, 0, 0, 0) + datetime.timedelta(days=i)
        total = 0
        for obj in objects:
            for i in range(len(new_tubes[obj]["values"])):
                if new_tubes[obj]["values"][i][0] == datetime.datetime.timestamp(today)*1000:
                    total = total + new_tubes[obj]["values"][i][1]
            
            
        new_tubes["total"]["values"].append([datetime.datetime.timestamp(today)*1000, total])
    
    # logging.warning(new_tubes["total"]["values"])

    return new_tubes

        

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
    sum_station_prod = float(prod_oxy) + float(prod_vac) + float(prod_comp)

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
        needed_data[obj]["cons3"] = needs.find_one({"object": obj})["m5"]
        needed_data["total"]["cons3"] = needed_data["total"]["cons3"] + needs.find_one({"object": obj})["m5"]
        
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

    needed_total_station = float(needed_data["total"]["oxy"]) + float(needed_data["total"]["comp"]) + float(needed_data["total"]["vac"])
    data_now = {}

    data_now["Проложено труб"] = str(round(100/float(needed_data["total"]["tubes"])*float(obj_data["total"]["tubes"]), 1)) + "%"
    data_now["Произведено консолей"] = str( round( 100/( float(needed_data["total"]["cons1"]) + float(needed_data["total"]["cons3"])) * ( float(consoles1) + float(consoles3)) , 1 ) ) + "%"
    data_now["Установлено консолей"] = str( round( 100/( float(needed_data["total"]["cons1"]) + float(needed_data["total"]["cons3"])) * ( float(obj_data["total"]["cons1"]) + float(obj_data["total"]["cons3"])) , 1 ) ) + "%"
    data_now["Произведено деталей в общем"] = str( round( 100/needed_total_station*sum_station_prod , 1) ) + "%"
    
    data_now["консоль1"] = {"надо": needed_data["total"]["cons1"], "есть": consoles1}
    data_now["консоль3"] = {"надо": needed_data["total"]["cons3"], "есть": consoles3}
    data_now["крб"] = {"надо": needed_data["total"]["krb"], "есть": krb}
    data_now["рш"] = {"надо": needed_data["total"]["rsh"], "есть": rsh}
    data_now["комп"] = {"надо": needed_data["total"]["comp"], "есть": comp_station}
    data_now["вак"] = {"надо": needed_data["total"]["vac"], "есть": vac_station}
    data_now["кис"] = {"надо": needed_data["total"]["oxy"], "есть": oxy_station}
    
    data_now["Произведено деталей"] = {"надо": needed_data["total"]["oxy"], "есть": prod_oxy}
    data_now["Доставлено деталей"] = {"надо": needed_data["total"]["oxy"], "есть": delv_oxy}

    data_now["vac_Произведено деталей"] = {"надо": needed_data["total"]["vac"], "есть": prod_vac}
    data_now["vac_Доставлено деталей"] = {"надо": needed_data["total"]["vac"], "есть": delv_vac}
    
    data_now["comp_Произведено деталей"] = {"надо": needed_data["total"]["comp"], "есть": prod_comp}
    data_now["comp_Доставлено деталей"] = {"надо": needed_data["total"]["comp"], "есть": delv_comp}

    data_now["Объекты"] = {"Общее": {
                "Проложено труб": {
                    "надо": needed_data["total"]["tubes"],
                    "есть": obj_data["total"]["tubes"]
                },
                "Установлено консолей 1": {
                    "надо": needed_data["total"]["cons1"],
                    "есть": obj_data["total"]["cons1"]
                },
                "Установлено консолей 3": {
                    "надо": needed_data["total"]["cons3"],
                    "есть": obj_data["total"]["cons3"]
                },
                "КРБ": {
                    "надо": needed_data["total"]["krb"],
                    "есть": obj_data["total"]["krb"]
                },
                "РШ": {
                    "надо": needed_data["total"]["rsh"],
                    "есть": obj_data["total"]["rsh"]
                },
                "Ваакум": {
                    "надо": needed_data["total"]["vac"],
                    "есть": obj_data["total"]["vac"]
                },
                "Воздух": {
                    "надо": needed_data["total"]["comp"],
                    "есть": obj_data["total"]["comp"]
                },
                "Кислород": {
                    "надо": needed_data["total"]["oxy"],
                    "есть": obj_data["total"]["oxy"]
                }
            }
        }
    
    for obj in objects:
        data_now["Объекты"][obj] = {
            "Проложено труб": {
                "надо": needed_data[obj]["tubes"],
                "есть": obj_data[obj]["tubes"]
            },
            "Установлено консолей 1": {
                "надо": needed_data[obj]["cons1"],
                "есть": obj_data[obj]["cons1"]
            },
            "Установлено консолей 3": {
                "надо": needed_data[obj]["cons3"],
                "есть": obj_data[obj]["cons3"]
            },
            "КРБ": {
                "надо": needed_data[obj]["krb"],
                "есть": obj_data[obj]["krb"]
            },
            "РШ": {
                "надо": needed_data[obj]["rsh"],
                "есть": obj_data[obj]["rsh"]
            },
            "Ваакум": {
                "надо": needed_data[obj]["vac"],
                "есть": obj_data[obj]["vac"]
            },
            "Воздух": {
                "надо": needed_data[obj]["comp"],
                "есть": obj_data[obj]["comp"]
            },
            "Кислород": {
                "надо": needed_data[obj]["oxy"],
                "есть": obj_data[obj]["oxy"]
            }
        }
    
    data_now["date"] = datetime.datetime.now().strftime("%d.%m")

    new_t = tubes_calc()

    data_now["tubes_data"] = new_t

    data_now_db.insert_one(data_now)


# Main page
@app.route("/", methods=["GET", "POST"])
@basic_auth.required
def index():
    calculate()
    return render_template(
        "index.html", **locals())


# Main page
@app.route("/test/", methods=["GET", "POST"])
def index2():
    calculate()
    return render_template(
        "test.html", **locals())


@socketio.on('connect', namespace='/test')
def test_connect():
    calculate()
    senddata = data_now_db.find_one(sort=[( '_id', pymongo.DESCENDING )])
    senddata["_id"] = 0
    emit('my response', senddata)


@app.route("/enter", methods=["GET", "POST"])
def enter():
    return render_template(
        "enter.html", **locals())


# Main flask app
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)