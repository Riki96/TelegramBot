import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
import time
import json
# from urllib2 import urlopen
import request

step = 1
def on_chat_message(msg):
	pprint(msg)
	global step
	content_type, chat_type, chat_id = telepot.glance(msg)
	if step == 1:
		keyboard = InlineKeyboardMarkup(inline_keyboard=[
				[
				InlineKeyboardButton(text='Book', callback_data='book'),
				InlineKeyboardButton(text='Order', callback_data='order')
				]
			])
		bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

	# isPresent, customer = search_customer(fil)
	if step == 2:
		# print('-------\n')
		# pprint(msg)
		# keyboard = InlineKeyboardMarkup(inline_keyboard=[
		# 		[
		# 		InlineKeyboardButton(text='Order', callback_data='book')
		# 		]
		# 	])
		# bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
		people = int(msg['text'])
		bot.sendMessage(chat_id, 'Ok...you are %d'%people)
		step = 3 # Booking - Time

	if step == 3:
		bot.sendMessage(chat_id, 'What time? (Please use hh-mm dd/mm format)')
		keyboard = InlineKeyboardMarkup(inline_keyboard=[
				[
				InlineKeyboardButton(text='19:00', callback_data='19:00 time'),
				InlineKeyboardButton(text='19:30', callback_data='19:30 time'),
				InlineKeyboardButton(text='20:00', callback_data='20:00 time'),
				InlineKeyboardButton(text='20:30', callback_data='20:30 time'),
				]
			])
		bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)		



def on_callback_query(msg):
	global step
	file = open_json('Customers.json')
	query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
	print(query_id, chat_id, query_data)

	# query_data = query_data.split(' ')[1]

	if query_data == 'book':
		bot.sendMessage(chat_id, 'Booking...')
		pprint(step)
		isPresent, customer = search_customer(file, msg)
		if isPresent:
			bot.sendMessage(chat_id, 'Booking already present')
			bot.sendMessage(chat_id, customer)
			# print(msg['from']['text'])
		else:
			# print(msg['from']['text'])
			step = 2 # Booking - People
			bot.sendMessage(chat_id, 'Booking...')
			# obj = create_json_booking(msg, step)
			# file['Customers'].append(obj)
			# write_json(file)
			# time.sleep(0.5)
			bot.sendMessage(chat_id, 'How many people?')

	if 'time' in query_data:
		print('ciao')
		time = query_data.split(' ')[0]
		bot.sendMessage(chat_id, 'Ok...the table will be ready for %s'%time)

		obj = create_json_booking(msg, time, people)
		step = 4 

	if query_data == 'order':
		step = 5

def open_json(file):
	with open(file, 'r') as file:
		obj = json.load(file)
	return obj

def write_json(obj):
	with open('Customers.json', 'w') as file:
		file.write(json.dumps(obj))

def create_json_booking(msg, step, time, people):
	id_name = msg['from']['id']
	nick_name = msg['from']['username']
	first_name = msg['from']['first_name']

	obj = {
		'id':id_name,
		'name':first_name,
		'nickname':nick_name,
		'step': step,
		'people':people,
		'time':time
	}

	return obj

def search_customer(file, msg):
	cust = file['Customers']
	id_name = msg['from']['id']

	isPresent = False
	customer = ''
	for c in cust:
		if c['id'] == id_name:
			isPresent = True
			customer = c

	return isPresent, customer

def get_step(file, msg):
	obj = open_json(file)
	customers = obj['Customers']
	customer = search_customer(file, msg)

	step = customer['step']
	return step


if __name__ == '__main__':

	TOKEN = '772524655:AAFBuu9bvaVTF_2e-vBJtv5j9sI-xG-C6fY'
	bot = telepot.Bot(TOKEN)
	MessageLoop(bot, {'chat':on_chat_message, 'callback_query':on_callback_query}).run_as_thread()
	pprint('Listening...')
	while 1:
		time.sleep(10)