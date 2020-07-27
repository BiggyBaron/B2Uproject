if message.reply_to_message.text == 'ДГКИБ: Количество произведенных консолей на 1 газ в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p1"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных консолей на 3 газа в общем?", reply_markup=markup)
        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных консолей на 3 газа в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p2"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных РШ в общем?", reply_markup=markup)

        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных РШ в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p3"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных КРБ в общем?", reply_markup=markup)

        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных КРБ в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p4"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных компрессорных станций в общем?", reply_markup=markup)

        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных компрессорных станций в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p5"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных ваакумных станций в общем?", reply_markup=markup)

        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных ваакумных станций в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p6"
            }
            dash.insert_one(msg)
            markup = types.ForceReply(selective=False)
            bot.send_message(message.chat.id, "ДГКИБ: Количество произведенных кислородных станций в общем?", reply_markup=markup)

        if message.reply_to_message.text == 'ДГКИБ: Количество произведенных кислородных станций в общем?':
            msg = {
            "from": str(message.chat.id),
            "time": message.date,
            "data": message.text,
            "object": "ДГКИБ",
            "type": "p7"
            }
            dash.insert_one(msg)
            bot.send_message(message.chat.id, "Спасибо!")