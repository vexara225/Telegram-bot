import telebot
from telebot import types
import sqlite3 

bot = telebot.TeleBot('Токен бота')

@bot.message_handler(commands=["start"])
def start_command(message):

  
    conn = sqlite3.connect("database.sql") 
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name VARCHAR(50),
        registration_date DATETIME,
        status BOOLEAN)""")
    
    conn.commit()
    cur.close()
    conn.close()

   
    markup = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton("Подписаться на автора", url="https://t.me/Vexara3")
    button3 = types.InlineKeyboardButton("Наш уютный чатик", url="https://t.me/Celestia_genshin_chat")
    markup.row(button2, button3)

    with open("photo/Banner_for_the_bot.jpg", "rb") as file:
            bot.send_photo(message.chat.id,file,caption=f"""<b>🌟Добро пожаловать, {message.from_user.first_name}!</b>
Чтобы начать пользоваться ботом, сначала создай свой профиль.
После этого ты сможешь находить других игроков и искать людей для совместной игры. \n \n ⤷ Нажми <u>«Создать профиль»</u>""",parse_mode="html",reply_markup=markup)



    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать профиль")
    btn2 = types.KeyboardButton("Открыть мой профиль")
    btn3 = types.KeyboardButton("Поиск путешественников")

    keyboard.row(btn1, btn2, btn3)     
  
    bot.send_message(message.chat.id,"Выберите подходящий вариант из списка ниже 👇",reply_markup=keyboard)   

@bot.message_handler(func=lambda message: message.text == "Создать профиль")
def create_profile(message):
    bot.send_message(message.chat.id,"Отлично, давай вместе создадим твой профиль!", reply_markup=types.ReplyKeyboardRemove())


    bot.send_message(message.chat.id, "Напиши свой никнейм")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()
    user_region(message)


def user_region(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🇪🇺 Европа")
    btn2 = types.KeyboardButton("🇺🇸 Америка")
    btn3 = types.KeyboardButton("🌏 Азия")
    btn4 = types.KeyboardButton("🇨🇳 Тайвань, Гонконг, Макао") 

    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)

    bot.send_message(message.chat.id, "Выбери регион на котором находится твой игровой профель", reply_markup=keyboard)

    bot.register_next_step_handler(message, save_region)

def save_region(message):
    region = message.text.strip()

    bot.send_message(message.chat.id,"Отправь свою фотографию",reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, users_photo)

def users_photo(message):
    if message.photo:
        bot.reply_to(message, "Фотография принята! ^^")
    else:
        bot.send_message(message.chat.id, "Пришлите именно фотографию!!!")
        bot.register_next_step_handler(message, users_photo)


@bot.message_handler(func=lambda message: message.text == "Открыть мой профиль")
def open_profile(message):
    bot.send_message(message.chat.id,"Добавь потом сюда ответ")

@bot.message_handler(func=lambda message: message.text == "Поиск путешественников")
def search_travelers(message):
    bot.send_message(message.chat.id,"Погнали")

@bot.message_handler()
def info(message):
    if message.text.lower() == "все команды":
        bot.send_message(message.chat.id, "Конечно, вот все команды:")


bot.polling(none_stop=True)
 
