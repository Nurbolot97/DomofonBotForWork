import telebot
import json
from time import sleep, time
from telebot import types
from decouple import config


bot = telebot.TeleBot(config("TOKEN"), parse_mode=None)

# Board1
make_action = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton("Узнать код по адресу", callback_data="know")
btn2 = types.InlineKeyboardButton("Добавить новый код", callback_data="write")
make_action.add(btn1, btn2)

# Board2
make_choose = types.InlineKeyboardMarkup(row_width=2)
yes = types.InlineKeyboardButton("Yes", callback_data="yes")
nop = types.InlineKeyboardButton("Not", callback_data="not")
make_choose.add(yes, nop)

# Starting func
@bot.message_handler(commands=["start"])
def get_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Здравствуйте! Добро пожаловать!")
    bot.send_message(chat_id, "Что вы хотели? Выберите нужное!", reply_markup=make_action)

# Help func
@bot.message_handler(commands=["help"])
def get_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Помощь в пути!")
    bot.send_photo(chat_id, open("/home/nurbolot/AddressBot/media/canva1.jpg", "rb"))

# Callback func
@bot.callback_query_handler(func=lambda call:True)
def get_action(call):
    chat_id = call.message.chat.id
    if call.data == "know":
        msg = bot.send_message(chat_id, "Введите название улицы и номер дома. Например: Декабристов12")
        bot.register_next_step_handler(msg, give_password)
    elif call.data == "write":
        bot.send_message(chat_id, "Хорошо!")
        msg = bot.send_message(chat_id, "Напишите сначала адрес, а потом через двоеточие код домофона без пробелов! Например: Пестеля8под1:1234")
        bot.register_next_step_handler(msg, get_password)
    elif call.data == "yes":
        bot.send_message(chat_id, "Хорошо, направляю вас на запись...")
        msg = bot.send_message(chat_id, "Напишите сначала адрес, а потом через двоеточие код домофона без пробелов! Например: Пестеля8под1:1234")
        bot.register_next_step_handler(msg, get_password)
    elif call.data == "not":
        bot.send_message(chat_id, "Тогда возвращаю вас на главное окно...", reply_markup=make_action)
    else:
        bot.send_message(chat_id, "Для помощи нажмите: /help")

# Get and write password to json
def get_password(message):
    chat_id = message.chat.id
    with open("house_password.json", "r") as file:
            check_house_pass = json.load(file)
            list_ = list(check_house_pass)
            house_address = message.text.split(":")[0]
            if house_address in list_:
                bot.send_message(chat_id, "Код для этого дома(подъезда) уже имеется", reply_markup=make_action)
            else:
                try:
                    house_pass = message.text.split(":")
                    house_pass_dict = dict.fromkeys([house_pass[0]], house_pass[1])
                    with open("house_password.json") as file:
                        data = json.load(file)
                        data.update(house_pass_dict)
                    with open("house_password.json", "w") as file:
                        json.dump(data, file)
                except Exception:
                    bot.send_message(chat_id, "Вы ввели данные некорректно. \n Просим ввезти данные как на примере!", reply_markup=make_action)

# Give password for users
def give_password(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Идет поиск кода домофона в базе...")
    sleep(1)
    try:
        with open("house_password.json", "r") as file:
            result = json.load(file)
        bot.send_message(chat_id, f"{result[message.text]}")
    except (KeyError, ValueError):
        bot.send_message(chat_id, "Вы возможно ввели адрес неправильно или \n кода от этого дома пока нету в нашей базе!")
        bot.send_message(chat_id, "Хотите записать код к этому дому?", reply_markup=make_choose)

# For some unrelevant message
@bot.message_handler(content_types=["text", "audio", "photo", "document", "video", "voice", "location", "contact", "sticker"])
def get_any_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Начать общение с ботом: /start, помощь: /help")
        
# Turn on funcs
def main():
    bot.polling()
    

if __name__ == "__main__":
    main()























