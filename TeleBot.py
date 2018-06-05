from flask import Flask
import simplejson as json
import requests

app = Flask(__name__)

URL = 'https://api.telegram.org/bot531159192:AAGRUYM3DLLX6V7huZ9yxLBa7n5SwtR9DE0/'

def write_json(date, filename='ansver.json'):
	with open(filename, 'w') as f:
		json.dump(date, f, indent=2, ensure_ascii=False)


def get_updates():
	#https://api.telegram.org/bot531159192:AAGRUYM3DLLX6V7huZ9yxLBa7n5SwtR9DE0/getUpdates
	url = URL + 'getUpdates'
	r = requests.get(url)
	#write_json(r.json())
	return r.json()

def send_message(chat_id, text='bla-bla-bla'):
	url = URL + 'sendMessage'
	answer = {'chat_id': chat_id, 'text': text}
	r = requests.post(url, json=answer)
	return r.json()

@app.route('/')
def index():
	return '<h1>Hello bot</h1>'

def main():
	#r = requests.get(URL + 'getMe')
	#write_json(r.json())
	#r = get_updates()
	#chat_id = r['result'][-1]['message']['chat']['id']
	#send_message(chat_id)
	pass

if __name__ == '__main__':
	#main()
	app.run()