from flask import Flask
from flask import request
from flask import jsonify
from telebot import types
from telepot.namedtuple import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters)
import polling
import telepot
import simplejson as json
import requests
import telebot
import logging
from json import dumps, loads, JSONEncoder, JSONDecoder

app = Flask(__name__)
bot = telebot.TeleBot('560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80')

URL = 'https://api.telegram.org/bot560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80/'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить мой номер", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,'Привет!\n Я - @cocopalmsalon_bot, личный помощник салона красоты "Коко Пальм"\n Рад тебя приветствовать! \n Для авторизации нажми, пожалуйста, кнопку "Отправить мой номер"', reply_markup=keyboard)


def handle_messages(messages):
	for message in messages:
		if message.contact is not None:
			bot.send_message(message.chat.id, 'Напиши свою дату рождения. Обещаю, я никому не скажу. Это будет нашим маленьким секретом (укажите свою дату рождения в формате ДД.ММ)')

bot.set_update_listener(handle_messages)


@bot.message_handler(content_types=["text"])
def keyboard_menu(message):
	if float(message.text):
		markup = types.ReplyKeyboardMarkup()
		markup.row('F.A.Q.', 'Заказать процедуру')
		markup.row('Отзывы о работе мастеров', 'Портфолио')
		markup.row('Хочу быть моделью')
		bot.send_message(message.chat.id, "Спасибо за регистрацию, добро пожаловать в главное меню!", reply_markup=markup)

if __name__ == '__main__':
	bot.polling(none_stop=True)
