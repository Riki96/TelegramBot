import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space
from telepot.delegate import include_callback_query_chat_id
from telepot.loop import MessageLoop
import time

class Test:
	def __init__(self):
		self.count = 0

	def add(self, n):
		self.count += n

	def output(self):
		return self.count


class Imaging:
	def __init__(self):
		pass

	def sendPhoto(self, bot):
		bot.sendPhoto('img.jpg')


class Tel_Bot(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(Tel_Bot, self).__init__(*args, **kwargs)
		self.test = Test()
		self.img = Imaging()

	def on_chat_message(self, msg):

		content_type, chat_type, chat_id = telepot.glance(msg)

		print(chat_id)

		if msg['text'] == 'add':
			self.test.add(1)
			# print('ciao')

		if msg['text'] == 'res':
			print(self.test.output())

		if msg['text'] == 'photo':
			telepot.sendPhoto('img.jpg')


if __name__ == '__main__':

	TOKEN = '892866853:AAF3W2Dns7-Koiayk-2fuDgIDiFCfrLEfLw'

	bot = telepot.DelegatorBot(TOKEN,[
			include_callback_query_chat_id(
			pave_event_space())(per_chat_id(), create_open, Tel_Bot, timeout=100)
		])

	MessageLoop(bot).run_as_thread()

	# bot = telepot.Bot(TOKEN)
	# bot.message_loop(Tel_Bot)
	print('AOOOO')
	while 1:
		time.sleep(10)