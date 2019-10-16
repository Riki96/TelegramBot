# print('Funzia?')
import requests as req
url = 'http://127.0.0.1:8000/add'
obj = {
	'a':1,
	'b':5
}
request = req.get(url, params=obj)
print(request.text)
