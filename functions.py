import time
import json


def open_json(file):
	with open(file, 'r') as file:
		obj = json.load(file)
	return obj

def write_json(obj):
	with open('Customers.json', 'w') as file:
		file.write(json.dumps(obj, indent=4))

def create_json_booking(update, time, people):
	id_name = update.message.from_user.id
	if update.message.from_user.username:
		nick_name = update.message.from_user.username
	else:
		nick_name = ''
	first_name = update.message.from_user.first_name

	obj = {
		'id':id_name,
		'name':first_name,
		'nickname':nick_name,
		'people':people,
		'time':time
	}

	return obj

def search_customer(id_):
	file = open_json('Customers.json')
	cust = file['Customers']

	isPresent = False
	customer = ''
	for c in cust:
		if c['id'] == id_:
			isPresent = True
			customer = c
	return isPresent, customer

def get_step(file, msg):
	obj = open_json(file)
	customers = obj['Customers']
	customer = search_customer(file, msg)

	step = customer['step']
	return step

def random_key(length=12):
	import string
	import random

	letters = string.ascii_lowercase
	output = ''.join(random.choice(letters) for s in range(length))
	print(output)
	return output

def search_key(file, key):
	obj = open_json(file)
	tables = obj['Customers']
	hasKey = False
	for t in tables:
		if key == t['code']:
			hasKey = True

	return hasKey


def hour2seconds(h):
	return h.split(':')[0]*3600 + h.split(':')[1]*60

def search_table(file, people, time):
	from collections import OrderedDict
	slots = file['Slots']

	wanted_slot = slots[time]
	# print('WANTED: ',wanted_slot)
	availables = [k for k,v in wanted_slot.items() if v['status'] == 0 and v['size'] >= people]
	if len(availables) > 0:
		# print('AHOOOOOOOOOOOOOOOOOO')
		return availables[0], None, None
	else:
		nexts = []
		# x = OrderedDict()
		# index_wanted = 
		for k,v in slots.items():
			if hour2seconds(k) > hour2seconds(wanted_slot.items()[0]):
				news = [kk for kk,vv in k.items() if vv['status'] == 0 and v['size'] >= people]
				nexts.append((news[0], k))
		if len(nexts) > 0:
			return None, nexts[0][0], nexts[0][1]
		else:
			return None, None, None


def update_tables(file, time, table):
	found = 0
	for k,v in file['Slots'].items():
		cnt = 0
		if k == time or found == 1:
			found = 1
			file['Slots'][k][table]['status'] = 1
			cnt += 1
			if cnt == 3:
				found = 0
				break

	write_json(file)


def food_buttons(foods_list):
	from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

	key = []
	for f in foods_list:
		visualize = f['dish'] + ' - ' + str(f['cost']) + '$'
		code = 'ordered' + ':' + f['code']
		key = key + [InlineKeyboardButton(text=visualize, callback_data=code)]
	keyboard_output = InlineKeyboardMarkup(inline_keyboard=[[k] for k in key])

	return keyboard_output

def create_food_list(file, type_food):
	food_list = []
	menu = file['Menu']
	for m in menu:
		print(m['type'], type_food)
		if str(m['type']).lower() == str(type_food).lower():
			food_list.append(m)

	return food_list

def search_food(file, code):
	menu = file['Menu']
	for m in menu:
		if code == m['code']:
			return m
	
def integerizer(i):
	return int(i)	

def available_hour(file, time):
	tables = file['Tables']
	free_tables = [k for k,v in tables.items() if v['Status'] == 0]
	other_free = [k for k,v in tables.items() if v['Status'] == 1 and v['Time'] != time]
	free = free_tables + other_free
	free.sort(key=integerizer)

	available = False
	if len(free) > 0:
		available = True

	return available