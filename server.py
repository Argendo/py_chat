from flask import Flask, request, Response
import time

app = Flask(__name__)

messages = [
	
]

@app.route("/send", methods=['POST'])
def send():
	name = request.json.get('name')
	text = request.json.get('text')
	if not (name and isinstance(name, str) and text and isinstance(text, str)):
		return Response(status = 400)
	message = {'name': name, 'text': text, 'time': time.time()}
	messages.append(message)
	return Response(status=200)
	
def filtered_by_key(elements, key, thereshold):

	filtered_elements = []

	for element in elements:
		if element[key]>thereshold:
			filtered_elements.append(element)

	return filtered_elements

@app.route("/messages")
def messages_view():
	try:
		after=float(request.args['after'])
	except:
		return Response(status=400)
	filtered = filtered_by_key(messages, key='time', thereshold=after)
	return {'messages': filtered}


@app.route("/")
def hello():
	return "Hi there <br> <a href='/status'>Status</a>"

@app.route("/status")
def status():
	return{
		"name": "py_chat",
		"status": True,
		"time": datetime.now()
	}

app.run()
