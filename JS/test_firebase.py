import pyrebase as pb

key = 'AIzaSyDCXWiAe7bmEYrtL0GoI2-cOXpOKCeBdqM'
name_projecy = 'SmartRestaurantIoT'
id_project = 'smartrestaurantiot'

config = {
	'apiKey': key,
	'authDomain': id_project+'.firebaseapp.com',
	'databaseURL': 'https://smartrestaurantiot.firebaseio.com',
	'storageBucket': id_project+'.appspot.com'
}
mail = 'sappariccardo@gmail.com'
password = input('Insert password:\n-')
firebase = pb.initialize_app(config)
auth = firebase.auth()
# print(auth)
user = auth.sign_in_with_email_and_password(mail, password)
print(user)
db = firebase.database()
rest_1 = {
	'name': 'A Casa di Pulcinella',
	'address': 'Corso Carlo Rosselli, 82',
	'type': 'Pizzeria'
}

results = db.child('users').push(rest_1, user['idToken'])