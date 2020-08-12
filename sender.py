import requests


name = input("Your name: ")
password = input("Password: ")

while True:
    text = input("text: ")
    message = {'name':name,'text':text,'password':password}
    response = requests.post('http://127.0.0.1:5000/send',json=message)
