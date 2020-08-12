import time
import requests
from datetime import datetime

after = time.time() - 24 * 60 * 60  # отображаем сообщения за последний день


def format_message(message):
    name = message['name']
    text = message['text']
    dt = datetime.fromtimestamp(message['time'])
    time = dt.strftime("Message sent on %d-%m-%Y at %H:%M:%S")
    return f'{name} {time}\n{text}\n'


while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages', params={'after': 0})
    messages = response.json()['messages']
    for message in messages:
        print(format_message(message))
        after = message['time']
    time.sleep(1)
