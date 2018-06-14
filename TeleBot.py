from flask import Flask
from flask import request
from flask import jsonify
from telebot import types
import simplejson as json
import requests
import telebot

app = Flask(__name__)
bot = telebot.TeleBot('560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80')

URL = 'https://api.telegram.org/bot560420481:AAGSBQpupKG7fzhUkr905FuW6u-ORFvVK80/'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Привет!\n Я - @cocopalmsalon_bot, личный помощник салона красоты "Коко Пальм"\n Рад тебя приветствовать! \n Для авторизации нажми, пожалуйста, кнопку "Отправить мой номер"')
    bot.get_updates

@bot.message_handler(content_types=["text"])
def any_msg(message):
keyboard = types.InlineKeyboardMarkup()
	like_button= types.InlineKeyboardButton(text="Отправить мой номер", callback_data='like')
	keyboard.add(like_button)
	bot.send_photo(message.from_user.id,img, reply_markup=keyboard)

#ФУНКЦИЯ КОТОРАЯ ПРИНЕМАЕТ ДАННЫЕ
def write_json(date, filename='ansver.json'):
	with open(filename, 'w') as f:
		json.dump(date, f, indent=2, ensure_ascii=False)

#ПОЛУЧЕНИЕ ДАННЫХ ОТ ТЕЛЕГРАМА
def get_updates():
	#https://api.telegram.org/bot531159192:AAGRUYM3DLLX6V7huZ9yxLBa7n5SwtR9DE0/getUpdates
	url = URL + 'getUpdates'
	r = requests.get(url)
	#write_json(r.json())
	return r.json()

#ФУНКИЯ ДЛЯ ОТВЕТА бОТА
def send_message(chat_id, text='bla-bla-bla'):
	url = URL + 'sendMessage'
	answer = {'chat_id': chat_id, 'text': text}
	r = requests.post(url, json=answer)
	return r.json()

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		r = request.get_json()
		chat_id = r['message']['chat']['id']
		message = r['message']['text']

	if 'Здравствуйте' in message:
		send_message(chat_id, text='Здравствуйте')

		#whrite_json(r)
		return jsonify(r)

	return '<h1>Bot welcomes you</h1>'

	#https://api.telegram.org/bot531159192:AAGRUYM3DLLX6V7huZ9yxLBa7n5SwtR9DE0/setWebhook?url=https://daa08a0a.ngrok.io/


def main():
	#r = requests.get(URL + 'getMe')
	#write_json(r.json())
	#r = get_updates()
	#chat_id = r['result'][-1]['message']['chat']['id']
	#send_message(chat_id)
	pass

if __name__ == '__main__':
    bot.polling(none_stop=True)
