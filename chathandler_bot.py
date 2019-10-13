from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import json
from functions import *
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
class SmartRestaurant():
	def __init__(self):
		self.SET_OPT, self.BOOK, self.ORDER, self.PEOPLE, self.TIME = range(5)
		self.STATE = self.SET_OPT

	def start(self, bot, update):
		keyboard = [['Book', 'Order']]
		message = 'Welcome to RestaurantBot. Please select an option from the keyboard.'
		reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

		update.message.reply_text(message, reply_markup=reply_markup)

		return self.SET_OPT

	def help_(self, bot, update):
		message = 'You chose HELP! With thi bot you can select:\n- /start to initialize\n- /help for helping\n- Book to start booking\n- Order to start ordering.'	
		update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

	def cancel(self, bot, update):
	    """
	    User cancelation function.
	    Cancel conersation by user.
	    """
	    user = update.message.from_user
	    logger.info("User {} canceled the conversation.".format(user.first_name))
	    message = 'Conversation Ended! Come back soon!'
	    update.message.reply_text(message,
	                              reply_markup=ReplyKeyboardRemove())

	    return ConversationHandler.END

	def set_state(self, bot, update):
		if update.message.text == 'Book':
			print('BOOK')
			self.STATE = self.BOOK
			self.book(bot, update)
			return self.PEOPLE
		elif update.message.text == 'Order':
			print('ORDER')
			self.STATE = self.ORDER
			self.order(bot, update)
			return
		else:
			self.STATE = self.MENU
			print('MENU')
			return

	def book(self, bot, update):
		"""
		Booking phase: need to know time and number of people
		"""
		id_ = update.message.from_user.id
		is_present, customer = search_customer(id_)
		if is_present:
			message = 'You already have a booking! {}'.format(customer)
			update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
			return ConversationHandler.END
		else:
			logger.info('Requested Book by {}'.format(update.message.from_user))
			message = 'You have started the Booking phase! Please, let us know all the information needed!\n First, how many people are you booking for?'
			update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
			NEEDEDNOW = update.message.text
			return

	def people(self, bot, update):
		user = update.message.from_user.id
		self.BOOKED_PEOPLE = update.message.text
		logger.info('{} is booking for {} people'.format(user, self.BOOKED_PEOPLE))
		message = 'Perfect, {}, now let us know when do you intend to come?'.format(update.message.from_user.first_name)
		keyboard = [['Monday', 'Tuesday', 'Wednesday']]
		reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
		update.message.reply_text(message, reply_markup=reply_markup)
		return self.TIME

	def time(self, bot, update):
		logger.info('{} wants to come {}'.format(update.message.from_user.id, update.message.text))
		self.BOOKED_DAY = update.message.text
		message = 'Thanks! Your booking for {} for {} people is done!'.format(self.BOOKED_DAY, self.BOOKED_PEOPLE)
		update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
		obj = create_json_booking(update, self.BOOKED_DAY, self.BOOKED_PEOPLE)
		file = open_json('Customers.json')
		file['Customers'].append(obj)
		write_json(file)
		return ConversationHandler.END

	def order(self, bot, update):
		logger.info('Order phase by {}'.format(update.message.from_user.id))
		message = 'Please click on the link to start ordering'
		update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

	def main(self):
		updater = Updater('892866853:AAF3W2Dns7-Koiayk-2fuDgIDiFCfrLEfLw')

		# Get the dispatcher to register handlers:
		dp = updater.dispatcher
		conv_handler = ConversationHandler(
			entry_points=[CommandHandler('start',self.start)],
			states={
				self.SET_OPT: [RegexHandler('^(Book|Order)$',self.set_state)],
				self.BOOK: [RegexHandler('Book',self.book)],
				self.PEOPLE: [MessageHandler(Filters.regex('^[0-9]+$'), self.people)], #[0-9]+ regex for positive integers
				self.TIME: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday)$'), self.time)]
			},
			fallbacks=[CommandHandler('help',self.help_),
						CommandHandler('cancel', self.cancel)],
			allow_reentry=True
		)

		dp.add_handler(conv_handler)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	sr = SmartRestaurant()
	sr.main()





