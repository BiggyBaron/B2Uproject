if message.reply_to_message.text == 'ДГКИБ: Количество проложенных труб в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных КРБ в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных КРБ в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m2"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных РШ в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных РШ в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m3"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных консолей на 1 газ в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных консолей на 1 газ в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m4"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных консолей на 3 газа в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных консолей на 3 газа в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m5"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных ваакумных станций в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных ваакумных станций в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m6"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных станций сжатого воздуха в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных станций сжатого воздуха в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m7"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество установленных кислородных станций в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество установленных кислородных станций в общем?':
            msg = {
            "from": str(message.chat.id),
            "object": "ДГКИБ",
            "time": message.date,
            "data": message.text,
            "type": "m8"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ЦФ: Количество проложенных труб в общем?", reply_markup=markup)