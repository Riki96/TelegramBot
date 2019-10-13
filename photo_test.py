import telepot
import time

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	if msg['text'] == 'photo':
		bot.sendPhoto(chat_id, open('kidsseeghost.jpg','rb'))


TOKEN = '772524655:AAFBuu9bvaVTF_2e-vBJtv5j9sI-xG-C6fY'

bot = telepot.Bot(TOKEN)
# MessageLoop(bot).run_as_thread()
bot.message_loop(on_chat_message)
print('Listening...')

while 1:
    time.sleep(10)