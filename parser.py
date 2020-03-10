
import random,time
import requests
from bs4 import BeautifulSoup
import csv
import re
import checker
import follow 


import telebot



bot = telebot.TeleBot('755244271:AAEWLTazCjxuDctI6oBjhZZpAuvMTiauIlo')




@bot.message_handler(commands=['password'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, начинаем парсить")
    checker.main()
    bot.send_message(message.from_user.id,checker.result())
@bot.message_handler(commands=['download'])
def send_file(message):  
    try:
        doc = open('property.csv', 'rb') 
        bot.send_document(message.from_user.id, doc)
    except:
        bot.send_message(message.from_user.id,'Документ не составлен')
@bot.message_handler(commands=['follow'])
def send_item(message):
    bot.send_message(message.from_user.id,follow.main())       
       

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(10)