# https://pypi.org/project/pyTelegramBotAPI/0.3.0/
# pip install pyTelegramBotAPI

# https://pypi.org/project/pyowm/
# pip install pyowm


import telebot
import pyowm

owm = pyowm.OWM('ЗГЕНЕРУЙ КЛЮЧ')
token='5011504057:AAH8O8b3g2VweQGmHlrUE5UE1WonSfv6Wko'

bot = telebot.TeleBot(token)
mgr = owm.weather_manager()


@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, "Привет, введи город, а я покажу погоду")



@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather

    '''
    w.detailed_status         # 'clouds'
    w.wind()                  # {'speed': 4.6, 'deg': 330}
    w.humidity                # 87
    w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.rain                    # {}
    w.heat_index              # None
    w.clouds                  # 75
    '''

    temp = w.temperature('celsius')["temp"]

    answer = "В городе " + message.text + " сейчас " + w.detailed_status + "\n"
    answer += "Температура: " + str(temp) 

    bot.send_message(message.chat.id, answer)
    

bot.infinity_polling()
