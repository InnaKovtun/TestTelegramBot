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
import os
import random

app = Flask(__name__)
bot = telebot.TeleBot('560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80')

URL = 'https://api.telegram.org/bot560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80/'

photo_paths = []
current_photo_index = None
photo_message_id = None

STATE_WAITING_FOR_START_COMMAND = "waiting for start command"
STATE_RECEIVED_START_COMMAND = "received start command"
STATE_ASKED_FOR_PHONE_NUMBER = "asked for phone number"
STATE_RECEIVED_PHONE_NUMBER = "received phone number"
STATE_PRINTED_RECEIVED_PHONE_NUMBER = "printed received phone number"
STATE_ASKED_FOR_DATE_OF_BIRTH = "state asked for date of birth"
STATE_RECEIVED_DATE_OF_BIRTH = "received date of birth"
STATE_MAIN_MENU_OUTPUT = "main menu output"

STATE_CATEGORIES_OF_PROCEDURES_OUTPUT = "output categories of pocedures"
STATE_PROCEDURE_TYPES_OUTPUT = "output procedure types"
STATE_CHOICE_OF_PROCEDURE = "choice of procedure"

STATE_MEN_HAIRCUTS = "men's haircuts"
STATE_WOMEN_HAIRCUTS = "women's haircuts"
STATE_MANICURE_PROCEDURE = "manicure procedure"
STATE_PEDICURE_PROCEDURE = "pedicure procedure"
STATE_COSMETOLOGY = "cosmetology"
STATE_EPILATION_FEMALE = "epilation female"
STATE_EPILATION_MALE = "epilation male"
STATE_SOLARIUM = "solarium"
STATE_SHUGARING_FEMALE = "shugaring female"
STATE_SHUGARING_MALE = "shugaring male"
STATE_EYEBROWS_EYELASHES = "eyebrows and eyelashes"
STATE_TATTOOING = "tatooing"
STATE_TEETH_WHITENING = "teeth whitening"
STATE_MAKEUP_PROCEDURE = "makeup procedure"

STATE_ASKED_FOR_COMMENT = "asked for the comment"
STATE_RECEIVED_COMMENT = "recieved comment"
STATE_ANSWER_TO_COMMENT = "anwer to the comment"

STATE_ASKED_FOR_QUESTION = "asked for question"
STATE_RECEIVED_QUESTION = "received question"
STATE_ANSWER_TO_QUESTION = "answer to the question"

STATE_PORTFOLIO_OUTPUT = "output portfolio"
STATE_PORTFOLIO_TYPES_OUTPUT = "portfolio types output"
STATE_PORTFOLIO_TYPE_CHOOSE = "choose porttfolio type"
STATE_SHOWING_PHOTOS = "showing photos"

STATE_REVIEWS_OUTPUT = "output reviews"
STATE_NEXT_REVIEW_OUTPUT = "output next review"

STATE_OUTPUT_TYPES_OF_MODELING = "output types of modeling"
STATE_CHOOSE_TYPE_OF_MODELING = "choose type of modeling"
STATE_COLORATION_MODELING = "colorayion modeling choosed"
STATE_COLORATION_MODELING_Q = "coloration modeling q"
STATE_HAIRSTYLE_MODELING = "hairstyle modeling choosed"
STATE_HAIRSTYLE_MODELING_Q = "hairstyle modeling q"
STATE_MAKEUP_MODELING = "makeup modeling choosed"
STATE_MAKEUP_MODELING_Q = "makeup modeling q"

current_state = STATE_WAITING_FOR_START_COMMAND

def transition(from_state, to_state, data=None):
    print(from_state, "->", to_state)

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_PROCEDURE_TYPES_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_CHOICE_OF_PROCEDURE and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_ASKED_FOR_COMMENT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_RECEIVED_COMMENT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_ANSWER_TO_COMMENT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state


    if current_state == STATE_ASKED_FOR_QUESTION and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_RECEIVED_QUESTION and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state
    
    if current_state == STATE_ANSWER_TO_QUESTION and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_PORTFOLIO_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_PORTFOLIO_TYPES_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_PORTFOLIO_TYPE_CHOOSE and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_REVIEWS_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_NEXT_REVIEW_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_OUTPUT_TYPES_OF_MODELING and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_CHOOSE_TYPE_OF_MODELING and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_SHOWING_PHOTOS and to_state == STATE_PORTFOLIO_TYPE_CHOOSE:
        return to_state

    if current_state == STATE_SHOWING_PHOTOS and to_state == STATE_PORTFOLIO_TYPES_OUTPUT:
        return to_state

    if current_state == STATE_WAITING_FOR_START_COMMAND and to_state == STATE_RECEIVED_START_COMMAND:
        return to_state

    if current_state == STATE_RECEIVED_START_COMMAND and to_state == STATE_ASKED_FOR_PHONE_NUMBER:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить мой номер", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(
            data.chat.id,
            'Привет!\n Я - @cocopalmsalon_bot, личный помощник салона красоты "Коко Пальм"\n Рад тебя приветствовать! \n Для авторизации нажми, пожалуйста, кнопку "Отправить мой номер"',
            reply_markup=keyboard
        )
        return to_state

    if current_state == STATE_ASKED_FOR_PHONE_NUMBER and to_state == STATE_RECEIVED_PHONE_NUMBER:
        return to_state

    if current_state == STATE_RECEIVED_PHONE_NUMBER and STATE_ASKED_FOR_DATE_OF_BIRTH:
        bot.send_message(
            data.chat.id, 
            'Напиши свою дату рождения. Обещаю, я никому не скажу. Это будет нашим маленьким секретом (укажите свою дату рождения в формате ДД.ММ)'
        )
        return to_state

    if current_state == STATE_ASKED_FOR_DATE_OF_BIRTH and to_state == STATE_RECEIVED_DATE_OF_BIRTH:
        return to_state 

    if current_state == STATE_RECEIVED_DATE_OF_BIRTH and to_state == STATE_MAIN_MENU_OUTPUT:
        markup = types.ReplyKeyboardMarkup()
        markup.row("F.A.Q.", "Заказать процедуру")
        markup.row("Отзывы о работе мастеров", "Портфолио")
        markup.row("Хочу быть моделью")
        bot.send_message(data.chat.id, "Спасибо за регистрацию, добро пожаловать в главное меню!", reply_markup=markup)
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Мужские стрижки", callback_data="Мужские стрижки")
        button_2 = types.InlineKeyboardButton(text = "Женские стрижки", callback_data="Женские стрижки")
        button_3 = types.InlineKeyboardButton(text = "Маникюр", callback_data="Маникюр")
        button_4 = types.InlineKeyboardButton(text = "Педикюр", callback_data="Педикюр")
        button_5 = types.InlineKeyboardButton(text = "Косметология", callback_data="Косметология")
        button_6 = types.InlineKeyboardButton(text = "SHR-эпиляция женский зал", callback_data="SHR-эпиляция женский зал")
        button_7 = types.InlineKeyboardButton(text = "SHR-эпиляция мужской зал", callback_data="SHR-эпиляция мужской зал")
        button_8 = types.InlineKeyboardButton(text = "Солярий", callback_data="Солярий")
        button_9 = types.InlineKeyboardButton(text = "Шугаринг женский зал", callback_data="Шугаринг женский зал")
        button_10 = types.InlineKeyboardButton(text = "Шугаринг мужской зал", callback_data="Шугаринг мужской зал")
        button_11 = types.InlineKeyboardButton(text = "БРОВИ И РЕСНИЦЫ", callback_data="БРОВИ И РЕСНИЦЫ")
        button_12 = types.InlineKeyboardButton(text = "Татуаж", callback_data="Татуаж")
        button_13 = types.InlineKeyboardButton(text = "Отбеливание зубов Smile ROOM", callback_data="Отбеливание зубов Smile ROOM")
        button_14 = types.InlineKeyboardButton(text = "Макияж", callback_data="Макияж")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        key.add(button_13)
        key.add(button_14)
        bot.send_message(data.chat.id, "Выберите категорию процедуры", reply_markup=key)
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_MEN_HAIRCUTS:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Модельная 600 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Комплекс мужской 800 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Детская до 7 лет 400 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Спортивная (под насадку) 400 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Наголо 250 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Окантовка 350 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Оформление усов 100 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Оформление бороды 300 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Тонирование бороды 450 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Тонирование волос от 700 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state  

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_WOMEN_HAIRCUTS:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Короткая 750 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Средняя длинна 1050 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Комплекс женский 1350 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Мытье головы 150 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Уходовая маска 150 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Стрижка кончиков 400 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Оформление чёлки 250 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Укладка феном 500-700 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Плетение кос от 500 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Вечерняя причёска 2000-2500 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Кератиновое выпрям. от 2500 руб.", callback_data="Процедура")
        button_12= types.InlineKeyboardButton(text = "Окрашивание волос от 3000 руб.", callback_data="Процедура")
        button_13 = types.InlineKeyboardButton(text = "Снятие цвета от 1500 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        key.add(button_13)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_MANICURE_PROCEDURE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Класический 500 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Аппаратный 500 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Комбинированный 500 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Мужской 650 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Покрытие шеллак 1000 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Укрепление пластины гелем 600 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Укрепление акрилом 350 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Европейский 450 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Японский 1200 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Детский 400 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Снятие гель-лака 250 руб.", callback_data="Процедура")
        button_12= types.InlineKeyboardButton(text = "Дизайн 50-100 руб. за 1 ноготь", callback_data="Процедура")
        button_13 = types.InlineKeyboardButton(text = "Наращивание гелем 2500 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        key.add(button_13)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_PEDICURE_PROCEDURE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Класический женский 1300 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Класический мужской 1600 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Кислотный женский 1600 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Кислотный мужской 1800 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Обработка пальцев ног 800 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Паравинотерапия ног, рук 400 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_COSMETOLOGY:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Механическая чистка лица 2000 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Ультразвук. чиска лица 1700 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Комбин.чистка лица 2500 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Пилинг по типу кожи 2000-3500 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Уход по типу кожи 2000-3500 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Буккальний массаж лица 1900 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Микроволновая терапия лица 900 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Терапия лицо+шея+декольте 1200 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Удаление татуажа 1500 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Удаление татуировок 1500 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Крабовый пилинг 3500 руб.", callback_data="Процедура")
        button_12 = types.InlineKeyboardButton(text = "Пирсинг от 1000 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_EPILATION_FEMALE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Классическое бикини 3100 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Глубокое бикини 5000 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Живот 1500-3200 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Ноги (бедра) 8300 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Ноги (голень) 4700 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Ноги полностью 9800 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Пальцы ног 900 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Подмышечные впадины 2300 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Руки до локтя 3700 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Руки полностью 5100 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Верхняя губа 950 руб.", callback_data="Процедура")
        button_12 = types.InlineKeyboardButton(text = "Шея 1200-2800 руб.", callback_data="Процедура")
        button_13 = types.InlineKeyboardButton(text = "Щеки 1800 руб.", callback_data="Процедура")
        button_14 = types.InlineKeyboardButton(text = "Подбородок 850 руб.", callback_data="Процедура")
        button_15 = types.InlineKeyboardButton(text = "Бакенбарды 1200 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        key.add(button_13)
        key.add(button_14)
        key.add(button_15)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_EPILATION_MALE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Бакенбарды 1200 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Щеки 2300 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Грудь 4700 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Живот полностью 5000-6600 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Живот нижняя часть 4800 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Ноги до колена 6600 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Ноги полностью 11200 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Пальцы ног 1800 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Подмышечные впадины 2700 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Руки до локтя 5000 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Руки полностью 7100 руб.", callback_data="Процедура")
        button_12 = types.InlineKeyboardButton(text = "Спина 9500 руб.", callback_data="Процедура")
        button_13 = types.InlineKeyboardButton(text = "Шея (задняя часть) 2300 руб.", callback_data="Процедура")
        button_14 = types.InlineKeyboardButton(text = "Шея (передняя часть) 2300 руб.", callback_data="Процедура")
        button_15 = types.InlineKeyboardButton(text = "Лицо полностью 4800 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        key.add(button_13)
        key.add(button_14)
        key.add(button_15)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_SOLARIUM:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Солярий 1 минута 20 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Абонемент на 100 минут 1700 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Абонемент на 50 минут 900 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_SHUGARING_FEMALE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Класический бикини 950 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Глубокое бикини 1500 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Голень 750 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Ноги полностью 1200 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Руки полностью 650 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Лицо 300 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Подмышки 450 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_SHUGARING_MALE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Грудь 1500 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Спина 1500 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Живот 1000 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Ноги полностью 2500 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Ноги голень 1400 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Ягодицы 750 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Руки полностью 1150 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Руки до локтя 750 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Лицо 500 руб.", callback_data="Процедура")
        button_10 = types.InlineKeyboardButton(text = "Подмышки 650 руб.", callback_data="Процедура")
        button_11 = types.InlineKeyboardButton(text = "Класическое бикини 2500 руб.", callback_data="Процедура")
        button_12 = types.InlineKeyboardButton(text = "Глубокое бикини 4000 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        key.add(button_10)
        key.add(button_11)
        key.add(button_12)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_EYEBROWS_EYELASHES:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Наращивание ресниц 1800 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Наращивание ресниц 2д 2000 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Наращивание ресниц 3д 2300 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Снятие нарощеных ресниц 400 руб.", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Ламинирование ресниц 1900 руб.", callback_data="Процедура")
        button_6 = types.InlineKeyboardButton(text = "Коррекция бровей 300 руб.", callback_data="Процедура")
        button_7 = types.InlineKeyboardButton(text = "Окрашивание бровей краской 300 руб.", callback_data="Процедура")
        button_8 = types.InlineKeyboardButton(text = "Окрашивание бровей хной 500 руб.", callback_data="Процедура")
        button_9 = types.InlineKeyboardButton(text = "Ламинирование бровей 1100 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        key.add(button_7)
        key.add(button_8)
        key.add(button_9)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_TATTOOING:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Татуаж бровей 5500 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Татуаж губ 6500 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Татуаж глаз 4500 руб.", callback_data="Процедура")
        button_4 = types.InlineKeyboardButton(text = "Коррекция - 59% от стоимости", callback_data="Процедура")
        button_5 = types.InlineKeyboardButton(text = "Худ. татуировка от 3500 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_TEETH_WHITENING:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Экспресс 2550 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Двойное 3600 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Максимальное 3900 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_CATEGORIES_OF_PROCEDURES_OUTPUT and to_state == STATE_MAKEUP_PROCEDURE:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Макияж Дневной 1700 руб.", callback_data="Процедура")
        button_2 = types.InlineKeyboardButton(text = "Вечерний 2000 руб.", callback_data="Процедура")
        button_3 = types.InlineKeyboardButton(text = "Свадебный 2000-2500 руб.", callback_data="Процедура")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        bot.send_message(data.message.chat.id,
            text= "Выберите процедуру которую хотите заказать",
            reply_markup=key
        )
        return to_state

    if current_state == STATE_MEN_HAIRCUTS or\
       current_state == STATE_WOMEN_HAIRCUTS or\
       current_state == STATE_MANICURE_PROCEDURE or\
       current_state == STATE_PEDICURE_PROCEDURE or\
       current_state == STATE_COSMETOLOGY or\
       current_state == STATE_EPILATION_FEMALE or\
       current_state == STATE_EPILATION_MALE or\
       current_state == STATE_SOLARIUM or\
       current_state == STATE_SHUGARING_FEMALE or\
       current_state == STATE_SHUGARING_MALE or\
       current_state == STATE_EYEBROWS_EYELASHES or\
       current_state == STATE_TATTOOING or\
       current_state == STATE_TEETH_WHITENING or\
       current_state == STATE_MAKEUP_PROCEDURE and\
       to_state == STATE_CHOICE_OF_PROCEDURE:
        return to_state  

    if current_state == STATE_CHOICE_OF_PROCEDURE and to_state == STATE_ASKED_FOR_COMMENT:   
        bot.send_message(data.message.chat.id,
        text = "Укажите дату которую хотите заказать процедуту и комментарий"
        )
        return to_state

    if current_state == STATE_ASKED_FOR_COMMENT and to_state == STATE_RECEIVED_COMMENT:
        return to_state

    if current_state == STATE_RECEIVED_COMMENT and to_state == STATE_ANSWER_TO_COMMENT:
        bot.send_message(data.chat.id,
            'Спасибо, вскоре с вами свяжется администратор.',
        )
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_REVIEWS_OUTPUT:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Следующий", callback_data="Следующий отзыв")
        key.add(button_1)
        bot.send_message(data.chat.id, "Darya\nМастер: Елена Федорова (визажист)\nМне все очень понравилось. На вечеринке я была на высоте. Благодарю.",
         reply_markup=key)
        return to_state
 
    if current_state == STATE_REVIEWS_OUTPUT and to_state == STATE_NEXT_REVIEW_OUTPUT: 
        return to_state

    if current_state == STATE_REVIEWS_OUTPUT and to_state == STATE_REVIEWS_OUTPUT: 
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_OUTPUT_TYPES_OF_MODELING:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Окрашивание", callback_data="Окрашивание")
        button_2 = types.InlineKeyboardButton(text = "Прическа", callback_data="Прическа")
        button_3 = types.InlineKeyboardButton(text = "Макияж", callback_data="Макияж")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        bot.send_message(data.chat.id, "Моделью какой категории хотите быть?", reply_markup=key)
        return to_state

    if current_state == STATE_OUTPUT_TYPES_OF_MODELING and to_state == STATE_COLORATION_MODELING:
        bot.send_message(data.message.chat.id, "Укажите пожалуйста длинну ваших волос.")
        return to_state

    if current_state == STATE_COLORATION_MODELING and to_state == STATE_COLORATION_MODELING_Q:
        return to_state

    if current_state == STATE_COLORATION_MODELING and to_state == STATE_COLORATION_MODELING:
        return to_state

    if current_state == STATE_COLORATION_MODELING_Q and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_COLORATION_MODELING_Q and to_state == STATE_OUTPUT_TYPES_OF_MODELING:
        return to_state

    if current_state == STATE_OUTPUT_TYPES_OF_MODELING and to_state == STATE_HAIRSTYLE_MODELING:
        bot.send_message(data.message.chat.id, "Укажите пожалуйста длинну ваших волос.")
        return to_state

    if current_state == STATE_HAIRSTYLE_MODELING and to_state == STATE_HAIRSTYLE_MODELING_Q:
        return to_state

    if current_state == STATE_HAIRSTYLE_MODELING and to_state == STATE_HAIRSTYLE_MODELING:
        return to_state

    if current_state == STATE_HAIRSTYLE_MODELING_Q and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_HAIRSTYLE_MODELING_Q and to_state == STATE_OUTPUT_TYPES_OF_MODELING:
        return to_state

    if current_state == STATE_OUTPUT_TYPES_OF_MODELING and to_state == STATE_MAKEUP_MODELING:
        bot.send_message(data.message.chat.id, "Укажите пожалуйста Ваш возраст.")
        return to_state

    if current_state == STATE_MAKEUP_MODELING and to_state == STATE_MAKEUP_MODELING:
        return to_state

    if current_state == STATE_MAKEUP_MODELING and to_state == STATE_MAKEUP_MODELING_Q:
        return to_state

    if current_state == STATE_MAKEUP_MODELING_Q and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_MAKEUP_MODELING_Q and to_state == STATE_OUTPUT_TYPES_OF_MODELING:
        return to_state

    if current_state == STATE_COLORATION_MODELING and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_HAIRSTYLE_MODELING and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_MAKEUP_MODELING and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_PORTFOLIO_OUTPUT:
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Окрашивание волос", callback_data="Окрашивание волос")
        button_2 = types.InlineKeyboardButton(text = "Ногти", callback_data="Ногти")
        button_3 = types.InlineKeyboardButton(text = "Мake-up", callback_data="Make-up")
        button_4 = types.InlineKeyboardButton(text = "Тату", callback_data="Тату")
        button_5 = types.InlineKeyboardButton(text = "Татуаж", callback_data="Татуаж")
        button_6 = types.InlineKeyboardButton(text = "Отбеливание зубов", callback_data="Отбеливание зубов")
        key.add(button_1)
        key.add(button_2)
        key.add(button_3)
        key.add(button_4)
        key.add(button_5)
        key.add(button_6)
        bot.send_message(data.chat.id, "Выберите портфолио", reply_markup=key)
        return to_state

    if current_state == STATE_MAIN_MENU_OUTPUT and to_state == STATE_ASKED_FOR_QUESTION:
        bot.send_message(data.chat.id, "Введите ваш вопрос, я постараюсь на него ответить.")
        return to_state

    if current_state == STATE_ASKED_FOR_QUESTION and to_state == STATE_RECEIVED_QUESTION:
        return to_state

    if current_state == STATE_RECEIVED_QUESTION and to_state == STATE_ANSWER_TO_QUESTION:
        return to_state

    if current_state == STATE_PORTFOLIO_OUTPUT and to_state == STATE_PORTFOLIO_TYPES_OUTPUT:
        return to_state
        
    if current_state == STATE_PORTFOLIO_TYPES_OUTPUT and to_state == STATE_SHOWING_PHOTOS or\
       current_state == STATE_SHOWING_PHOTOS and to_state == STATE_SHOWING_PHOTOS:
        if data.data == "Окрашивание волос":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото окрашивания")
        elif data.data == "Ногти":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото ногти")
        elif data.data == "Make-up":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото макияж")
        elif data.data == "Тату":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото тату")
        elif data.data == "Татуаж":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото татуаж")
        elif data.data == "Отбеливание зубов":
            init_photo_paths_and_current_photo_index("D:\\Фото Бот\\Фото отбеливание зубов")
        
        return to_state

    if current_state == STATE_SHOWING_PHOTOS and to_state == STATE_MAIN_MENU_OUTPUT:
        return to_state

    print("! UNKNOWN TRANSITION !")
    return from_state

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    global current_state
    current_state = transition(current_state, STATE_RECEIVED_START_COMMAND)
    current_state = transition(current_state, STATE_ASKED_FOR_PHONE_NUMBER, message)

def handle_messages(messages):
    global current_state

    for message in messages:
        if message.contact is not None:
            if current_state == STATE_ASKED_FOR_PHONE_NUMBER:
                current_state = transition(current_state, STATE_RECEIVED_PHONE_NUMBER)
                current_state = transition(current_state, STATE_ASKED_FOR_DATE_OF_BIRTH, message)
        
        if message.text == "Заказать процедуру":
            current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT)
            current_state = transition(current_state, STATE_CATEGORIES_OF_PROCEDURES_OUTPUT, message)
        elif message.text == "Отзывы о работе мастеров":
            current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT)
            current_state = transition(current_state, STATE_REVIEWS_OUTPUT, message)
        elif message.text == "Хочу быть моделью":
            current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT)
            current_state = transition(current_state, STATE_OUTPUT_TYPES_OF_MODELING, message)
        elif message.text == "Портфолио":
            current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT)
            current_state = transition(current_state, STATE_PORTFOLIO_OUTPUT, message)
        elif message.text == "F.A.Q.":
            current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT)
            current_state = transition(current_state, STATE_ASKED_FOR_QUESTION, message)
        elif current_state == STATE_ASKED_FOR_COMMENT:
            if message.text is not None:
                current_state = transition(current_state, STATE_RECEIVED_COMMENT)
                current_state = transition(current_state, STATE_ANSWER_TO_COMMENT, message)
        elif  current_state == STATE_COLORATION_MODELING:
            if message.text is not None:
                question_coloring(message)

        elif current_state == STATE_HAIRSTYLE_MODELING:
            if message.text is not None:
                question_hairstyle(message)

        elif current_state == STATE_MAKEUP_MODELING:
            if message.text is not None:
                question_makeup(message)
        else:
            text(message)
            answer_faq(message)       


bot.set_update_listener(handle_messages)

@bot.message_handler(content_types=["text"])
def keyboard_menu(message):
    global current_state
    if len(message.text) == 5 and message.text[0].isdigit() and message.text[1].isdigit() and message.text[2]=="." and message.text[3].isdigit() and message.text[4].isdigit():
        current_state = transition(current_state, STATE_RECEIVED_DATE_OF_BIRTH)
        current_state = transition(current_state, STATE_MAIN_MENU_OUTPUT, message)
    

def text(message):
    global current_state
    if current_state == STATE_ASKED_FOR_QUESTION:
        if message.text is not None:
            message.text = message.text.split()
            current_state = transition(current_state, STATE_RECEIVED_QUESTION)

questions_coloring = ["Укажите исходный цвет", "Окрашены ли волосы в настоящий момент?",
                             "Согласны ли вы на экспериментальное окрашивание, на усмотрение мастера?", 
                             "По возможности отправьте мне фото волос, или напишите Нет, для пропуска этого вопроса.", "Спасибо заявка принята."]

questions_hairstyle = ["Укажите пожалуйста оттенок волос (брюнетка, блондинка, шатенка, рыжая)","Спасибо, заявка принята."]

questions_makeup = ["Присутствует ли на лице перманентный макияж?", "Отправьте, пожалуйста, фото анфас.", "Спасибо, заявка принята."]

def question_coloring(message):
    global current_state

    bot.send_message(message.chat.id, questions_coloring[0])
    questions_coloring.pop(0)
    current_state = transition(current_state, STATE_COLORATION_MODELING, message)

    if not questions_coloring:
        current_state = transition(current_state, STATE_COLORATION_MODELING_Q, message)

def question_hairstyle(message):
    global current_state
    
    bot.send_message(message.chat.id, questions_hairstyle[0])
    questions_hairstyle.pop(0)
    current_state = transition(current_state, STATE_HAIRSTYLE_MODELING, message)

    if not questions_hairstyle:
        current_state = transition(current_state, STATE_HAIRSTYLE_MODELING_Q, message)

def question_makeup(message):
    global current_state

    bot.send_message(message.chat.id, questions_makeup[0])
    questions_makeup.pop(0)
    current_state = transition(current_state, STATE_MAKEUP_MODELING, message)

    if not questions_makeup: 
        current_state = transition(current_state, STATE_MAKEUP_MODELING_Q, message)

def answer_faq(message):
    global current_state 
    if current_state == STATE_RECEIVED_QUESTION:
        answers = ["Стрижка мужская модельная 600 руб.", "Комплекс мужской 800 руб", "Стрижка детская  до 7 лет 400 руб",
                    "Стрижка спортивная (под насадку) 400", "Стрижка наголо 250", "Окантовка 350", "Оформление усов 100",
                    "Оформление бороды 300", "Тонирование бороды 450", "Мужское тонирование волос от 700", "Женская стрижка короткая 750",
                    "Женская стрижка средняя длина 1050", "Комплекс женский 1350", "Мытье головы 150", "Уходовая маска 150", "Стрижка кончиков 400",
                    "Оформление челки 250", "Укладка волос феном 500-750", "Накручивание локонов 850-1000", "Выпрямление утюжком 500-750",
                    "Плетение кос от 500", "Вечерняя прическа 2000-2500", "Кератиновое выпрямление от 2500", "Реабилитация секущихся кончиков от 1000",
                    "Окрашивание волос от 3000", "Снятие цвета от 1500", "Маникюр классический, аппаратный, комбинированный 500",
                    "Маникюр мужской 650", "Покрытие шеллак 1000", "Укрепление ногтевой пластины гелем 600","Укрепление ногтевой пластины акрилом 350",
                    "Маникюр европейский 450", "Японский маникюр 1200", "Детский маникюр 400 руб", "Снятие гель-лака 250","Дизайн 50-100 за 1 ноготь",
                    "Наращивание ногтей гелем 2500", "Педикюр классический женский 1300", "Педикюр классический мужской 1600","Педикюр кислотный женский 1600",
                    "Педикюр кислотный мужской 1800", "Обработка пальцев ног 800", "Парафинотерапия ног, рук 400",
                    "Механическая чистка лица 2000","Ультразвуковая чистка лица 1700", "Комбинированная чистка лица 2500", "Пилинг по типу кожи 2000-3500",
                    "Уход по типу кожи 2000-3000", "Буккальный массаж лица 1900", "Микротоковая терапия лицо 900", "Микротоковая терапия лицо+шея+декольте 1200",
                    "Удаление татуажа от 1500", "Удаление татуировок от 1500", "Карбоновый пилинг 3500","Пирсинг от 1000",
                    "Классическое бикини 3100", "Глубокое бикини 5000", "Живот 1500-3200", "Ноги (бедра) 8300","Ноги (голень) 4700","Ноги полностью  9800",
                    "Пальцы ног 900", "Подмышечные впадины 2300", "Руки до локтя   3700", "Руки полностью  5100","Верхняя губа 950", "Шея 1200-2800",
                    "Щеки 1800", "Подбородок 850", "Бакенбарды  1200", "Эпиляция мужская - Бакенбарды 1200","Эпиляция мужская - Щеки 2300",
                    "Эпиляция мужская - Грудь 4700","Эпиляция мужская - Живот полностью 5000-6600",
                    "Эпиляция мужская - Живот нижняя часть до пупка  4800","Эпиляция мужская - Ноги до колена 6600",
                    "Эпиляция мужская - Ноги полностью 11200", "Депиляция мужская - Пальцы ног 1800","Депиляция мужская - Подмышечные впадины 2700",
                    "Депиляция мужская - Руки до локтя 5000", "Депиляция мужская - Руки полностью 7100","Депиляция мужская - Спина 9500",
                    "Шея (задняя часть) 2300", "Шея (передняя часть) 2300","Щеки 2300","Лицо полностью (щеки, подбородок, лоб, бакенбарды)  4800",
                    "1 минута 20 руб", "Абонемент на 100 минут 1700","Абонемент на 50 минут 900", "классическое бикини 950",
                    "глубокое бикини 1500", "голень  750", "ноги полностью 1200", "руки полностью  650", "лицо 300","подмышки 450",
                    "Мужской шугаринг грудь 1500", "Мужской шугаринг спина 1500", "Мужской шугаринг живот 1000",
                    "Мужской шугаринг ноги полностью  2500", "Мужской шугаринг ноги голень 1400", "Мужской шугаринг ноги бедра 1400",
                    "Мужской шугаринг ягодицы 750", "Мужской шугаринг руки полностью  1150", "Мужской шугаринг руки до локтя 750",
                    "Мужской шугаринг лицо 500", "Мужской шугаринг подмышки 650", "Мужской шугаринг классическое бикини 2500"
                    "Мужской шугаринг глубокое бикини 4000", "Наращивание ресниц классика 1800, 2д 2000, 3д 2300","Снятие наращенных ресниц 400",
                    "Ламинирование ресниц 1900","Коррекция бровей 300", "Окрашивание бровей краской 300", "Окрашивание бровей хной 500",
                    "Ламинирование бровей 1100", "Татуаж бровей (в любой технике) 5500", "Татуаж губ 6500", "Татуаж глаз 4500",
                    "Коррекция – 50% от стоимости первичного приема", "Художественная татуировка от 3500", "Экспресс отбеливание 2550",
                    "Двойное отбеливание 3600", "Максимальное отбеливание 3900", "Макияж Дневной 1700", "Вечерний макияж 2000", "Свадебный макияж 2000-2500"]
        all_answers = []
        for q_word in message.text:
            for answer in answers:
                words_in_answer = answer.split()
                for a_word in words_in_answer:
                    if q_word == a_word:
                        all_answers.append(answer)

        add_all_answers = '\n'.join(all_answers)                   
        
        if not add_all_answers:
            bot.send_message(message.chat.id, text = "Мы ничего не нашли по вашему вопросу, можете спросить у нашего администратора: @DaryaPetkevich")
        else:
            bot.send_message(message.chat.id, text = "Вот что мы нашли по вашему запросу:\n" + add_all_answers + 
            "\nЕсли это не то, что вы искали можете обратиться к нашему администратору: @DaryaPetkevich")

            
        current_state = transition(current_state, STATE_ANSWER_TO_QUESTION, message)

@bot.callback_query_handler(func=lambda call: True)
def model(call):
    #print("- CALL -")
    #print(call)
    #print("- - -")
    #print(" ")
    #print(" ")
    #print(" ")

    global current_state
    if call.data == "Мужские стрижки": 
        current_state = transition(current_state, STATE_MEN_HAIRCUTS, call)

    if call.data == "Женские стрижки":
        current_state = transition(current_state, STATE_WOMEN_HAIRCUTS, call)
            
    if call.data == "Маникюр":
        current_state = transition(current_state, STATE_MANICURE_PROCEDURE, call)
    
    if call.data == "Педикюр":
        current_state = transition(current_state, STATE_PEDICURE_PROCEDURE, call)
            
    if call.data == "Косметология":
        current_state = transition(current_state, STATE_COSMETOLOGY, call)

    if call.data == "SHR-эпиляция женский зал":
        current_state = transition(current_state, STATE_EPILATION_FEMALE, call)
       
    if call.data == "SHR-эпиляция мужской зал":
        current_state = transition(current_state, STATE_EPILATION_MALE, call)
        
    if call.data == "Солярий":
        current_state = transition(current_state, STATE_SOLARIUM, call)
    
    if call.data == "Шугаринг женский зал":
        current_state = transition(current_state, STATE_SHUGARING_FEMALE, call)
        
    if call.data == "Шугаринг мужской зал":
        current_state = transition(current_state, STATE_SHUGARING_MALE, call)
        
    if call.data == "БРОВИ И РЕСНИЦЫ":
        current_state = transition(current_state, STATE_EYEBROWS_EYELASHES, call)

    if call.data == "Татуаж":
        current_state = transition(current_state, STATE_TATTOOING, call)

    if call.data == "Отбеливание зубов Smile ROOM":
        current_state = transition(current_state, STATE_TEETH_WHITENING, call)

    if call.data == "Макияж":
        current_state = transition(current_state, STATE_MAKEUP_PROCEDURE, call)
        
    if call.data == "Процедура":
        current_state = transition(current_state, STATE_CHOICE_OF_PROCEDURE)
        current_state = transition(current_state, STATE_ASKED_FOR_COMMENT, call)

    if call.data == "Портфолио":
        current_state = transition(current_state, STATE_PORTFOLIO_OUTPUT)
        current_state = transition(current_state, STATE_PORTFOLIO_TYPES_OUTPUT, call)

    if call.data == "Окрашивание волос" or call.data == "Ногти" or call.data == "Make-up" or\
       call.data == "Тату" or call.data == "Татуаж" or call.data == "Отбеливание зубов":
        current_state = transition(current_state, STATE_PORTFOLIO_TYPES_OUTPUT)
        current_state = transition(current_state, STATE_SHOWING_PHOTOS, call)

        increment_current_photo_index()
        show_current_photo(call.message.chat.id)

    if call.data == "Окрашивание":
        current_state = transition(current_state, STATE_OUTPUT_TYPES_OF_MODELING )
        current_state = transition(current_state, STATE_COLORATION_MODELING, call)

    if call.data == "Прическа":
        current_state = transition(current_state, STATE_OUTPUT_TYPES_OF_MODELING )
        current_state = transition(current_state, STATE_HAIRSTYLE_MODELING, call)

    if call.data == "Макияж":
        current_state = transition(current_state, STATE_OUTPUT_TYPES_OF_MODELING )
        current_state = transition(current_state, STATE_MAKEUP_MODELING, call)

    if call.data == "Следующий отзыв":
        current_state = transition(current_state, STATE_REVIEWS_OUTPUT)
        REVIEWS = ["Дмитрий\nМастер: Евгения Больших (косметолог)\nХорошая работа, приятный персонал.",
         "Darya\nМастер: Елена Федорова (визажист)\nМне все очень понравилось. На вечеринке я была на высоте. Благодарю."]
        review = random.choice(REVIEWS)
        key = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text = "Следующий", callback_data="Следующий отзыв")
        key.add(button_1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = review, reply_markup=key)
        current_state = transition(current_state, STATE_REVIEWS_OUTPUT, call)
    
    if call.data == "Следующее (окраш)":
        #update_photo_message_id(call.message.message_id)
        increment_current_photo_index()
        show_current_photo(call.message.chat.id)

    if call.data == "Предыдущее (окраш)":
        #update_photo_message_id(call.message.message_id)
        decrement_current_photo_index()
        show_current_photo(call.message.chat.id)

def update_photo_message_id(new_photo_message_id):
    global photo_message_id
    photo_message_id = new_photo_message_id

def init_photo_paths_and_current_photo_index(directory):
    all_files_in_directory = os.listdir(directory)
    global photo_paths
    global current_photo_index
    photo_paths = []
    current_photo_index = None
    for file_name in all_files_in_directory:
        photo_path = directory + "\\" + file_name
        photo_paths.append(photo_path)

def increment_current_photo_index():
    global photo_paths
    global current_photo_index

    if current_photo_index is None:
        current_photo_index = 0
    else:
        current_photo_index = current_photo_index + 1

    if current_photo_index == len(photo_paths):
        current_photo_index = 0

def decrement_current_photo_index():
    global photo_paths
    global current_photo_index

    if current_photo_index is None:
        current_photo_index = 0
    else:
        current_photo_index = current_photo_index - 1

    if current_photo_index < 0:
        current_photo_index = len(photo_paths) - 1

def show_current_photo(chat_id):
    global photo_paths
    global current_photo_index
    global photo_message_id

    current_photo_path = photo_paths[current_photo_index]
    img = open(current_photo_path, 'rb')
    key = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text = "Предыдущее", callback_data="Предыдущее (окраш)")
    button_2 = types.InlineKeyboardButton(text = "Следующее", callback_data="Следующее (окраш)")
    key.add(button_1, button_2)
    if photo_message_id is not None:
        bot.delete_message(chat_id, photo_message_id)
    sent_photo_message = bot.send_photo(chat_id, img, reply_markup=key)
    update_photo_message_id(sent_photo_message.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
