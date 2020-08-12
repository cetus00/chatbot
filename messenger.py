import time
from datetime import datetime
import requests
from client_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sendButton.pressed.connect(self.send_message)

        self.after = time.time() - 500

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def print_error_message(self,msg):
        self.textBrowser.append(msg + "\n")

    def update_messages(self):
        try:
            print(requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}))
            data = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}).json()
        except:
            return

        for message in data['messages']:
            self.textBrowser.append(self.format_message(message))
            self.after = message['time']

    def format_message(self,message):
        name = message['name']
        text = message['text']
        dt = datetime.fromtimestamp(message['time'])
        time = dt.strftime("Message sent on %d-%m-%Y at %H:%M:%S")
        return f'{name} {time}\n{text}\n'

    def send_message(self):
        name = self.lineEditLogin.text()
        password = self.lineEditPassword.text()
        text = self.textEdit.toPlainText().strip()
        if not name or not password or not text:
            self.print_error_message('Please fill in the form before sending it')
            return

        message = {'name': name,
                   'text': text,
                   'password': password}
        try:
            response = requests.post('http://127.0.0.1:5000/send', json=message)
            print("Cnатус-код: ",response.status_code)
            if response.status_code == 200:
                self.textBrowser.append("Message sent successfully")
                self.textEdit.setText('')  # clear text editor after sending message
            elif response.status_code == 401:
                self.print_error_message('Unauthorised user')
            # else:
            #     self.print_error_message('Unknown error. Please reboot the app')
        except:
            self.print_error_message("Some error on the server")
            return






app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec_()