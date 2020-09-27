from PyQt5 import QtWidgets, QtCore
from datetime import datetime
import requests
import clientui

class MyWindow(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.send_button.pressed.connect(self.send_message)

		self.after = 0
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.load_messages)
		self.timer.start(1000)

	def clean_message(self, message):
		dt = datetime.fromtimestamp(message['time'])
		dt_str = dt.strftime('%H:%M:%S')
		self.messages.append(message['name'] + ' ' + dt_str)
		self.messages.append(message['text'])
		self.messages.append('')
		self.messages.repaint()

	def load_messages(self):
		try:
			data = requests.get('http://127.0.0.1:5000/messages', params={'after': self.after}).json()
		except:
			return

		for message in data['messages']:
			self.clean_message(message)
			self.after = message['time']

	def send_message(self):
		name = self.name_input.text()
		text = self.text_input.toPlainText()

		data={"name": name,	"text": text}
		try:
			response = requests.post('http://127.0.0.1:5000/send', json=data)
		except:
			self.messages.append("\nServer is not available :( \nTry later...\n")
			self.messages.repaint()
			return

		if response.status_code != 200:
			self.messages.append("\n\nBad data :(\n\n")
			self.messages.repaint()
			return

		self.text_input.setText('')
		self.text_input.repaint()

app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
