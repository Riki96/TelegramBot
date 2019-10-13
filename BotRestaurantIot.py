import telepot
import json


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        current_nickname = msg['from']['id']
        current_name = msg['from']['first_name']
        txt = msg['text']
        with open('Customers.json', 'r') as f:
            obj = json.load(f)

        customers = obj['Customers']
        print(customers)




if __name__ == '__main__':

    TOKEN = '772524655:AAFBuu9bvaVTF_2e-vBJtv5j9sI-xG-C6fY'

    bot = telepot.Bot(TOKEN)
    bot.message_loop(on_chat_message)

    print ('Listening ...')

    import time
    while 1:
        time.sleep(10)