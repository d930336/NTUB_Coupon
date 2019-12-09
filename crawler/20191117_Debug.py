import requests

url = "http://dde2b68d.ngrok.io/rest-auth/registration/"
post_data = {'username': 'jun','email':'10546027@ntub.edu.tw','password1':'as12345678','password2':'as12345678'}
respond = requests.post(url,data = post_data)
print(respond)