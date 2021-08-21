import telebot
import json
from time import sleep, time
from telebot import types
from decouple import config


bot = telebot.TeleBot(config("TOKEN"), parse_mode=None)

# KeyBoard1
make_action = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton("Узнать код по адресу", callback_data="know")
btn2 = types.InlineKeyboardButton("Добавить новый код", callback_data="write")
make_action.add(btn1, btn2)

# KeyBoard2
make_choose = types.InlineKeyboardMarkup(row_width=2)
yes = types.InlineKeyboardButton("Да  \U00002714", callback_data="yes")
nop = types.InlineKeyboardButton("Нет  \U0000274E", callback_data="not")
make_choose.add(yes, nop)

# KeyBoard3
make_change = types.InlineKeyboardMarkup(row_width=2)
yes1 = types.InlineKeyboardButton("Конечно", callback_data="yes1")
not1 = types.InlineKeyboardButton("Нет, воздержусь", callback_data="not1")
to_know = types.InlineKeyboardButton("Узнать код", callback_data="know")
make_change.add(yes1, not1, to_know)

# Starting func
@bot.message_handler(commands=["start"])
def get_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Добро пожаловать! \U0001F64B")
    bot.send_message(chat_id, "Что вы хотели? Выберите нужное!", reply_markup=make_action)

# Help func
@bot.message_handler(commands=["help"])
def get_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Данный бот предназначен для записи новых и\nвыдачи уже существующих кодов от домофонов.\nСледуйте всем инструкциям бота \U0001F609 \nчтобы не вредить на роботоспособность бота. Для старта нажмите: /start")
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
    elif call.data == "yes1":
        msg = bot.send_message(chat_id, "Отлично, тогда напишите адрес дома(с подъездом)\nу которого хотите изменить код и сам новый код.\nНапример: Декабристов21под3:1997")
        bot.register_next_step_handler(msg, make_pass_change)
    elif call.data == "not1":
        bot.send_message(chat_id, "Понятно, направляю вас на главное окно...", reply_markup=make_action)
    else:
        bot.send_message(chat_id, "Для помощи нажмите: \U000027A1 /help")

# To change exist password 
def make_pass_change(message):
    chat_id = message.chat.id
    with open("house_password.json", "r") as file:
        address = json.load(file)
        change_address = address[f"{message.text}"]
        
    
    

# Get and write password to json
def get_password(message):
    chat_id = message.chat.id
    house_pass = message.text.split(":")
    with open("house_password.json", "r") as file:
        check_house_pass = json.load(file)
        list_ = list(check_house_pass)
        house_address = message.text.split(":")[0]
        if house_address in list_:
            bot.send_message(chat_id, "Код для этого дома(подъезда) уже имеется \U0001F60B.\nХотите изменить код для данного адреса?", reply_markup=make_change)
        elif len(house_pass) == 2:
            house_pass_dict = dict.fromkeys([house_pass[0]], house_pass[1])
            with open("house_password.json") as file:
                data = json.load(file)
            data.update(house_pass_dict)
            with open("house_password.json", "w") as file:
                json.dump(data, file)
            bot.send_message(chat_id, "Код записан, спасибо! \U00002705", reply_markup=make_action)
        else:
            bot.send_message(chat_id, "Вы возможно поставили знак - (:) в нескольких местах или ввели данные некорректно.\U0001F632\nПросим ввезти данные как на примере!", reply_markup=make_action) 
   
                    

# Give password for users
def give_password(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Идет поиск кода домофона в базе...")
    sleep(1)
    try:
        with open("house_password.json", "r") as file:
            result = json.load(file)
        bot.send_message(chat_id, f"{result[message.text]}")
        bot.send_message(chat_id, "Хотите продолжить? \U0001F60A", reply_markup=make_action)
    except (KeyError, ValueError):
        bot.send_message(chat_id, "Вы возможно ввели адрес неправильно или \n кода от этого дома пока нету в нашей базе! \U0001F61E")
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























