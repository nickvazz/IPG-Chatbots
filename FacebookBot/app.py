# https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
# https://www.twilio.com/blog/2018/02/facebook-messenger-bot-heroku-python-flask.html
# https://www.twilio.com/blog/extending-your-flask-app-with-an-api

import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

with open('access_token.txt') as f:
	ACCESS_TOKEN = f.readline().replace('\n','')

VERIFY_TOKEN = "test-token"
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return varify_fb_token(token_sent)

	else:
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					recipient_id = message['sender']['id']
					print (message)
					print (message.get('message'))
					if message['message'].get('text'):
						response_sent_text = get_message()
						send_message(recipient_id, response_sent_text)

					if message['message'].get('attachments'):
						response_sent_nontext = get_message()
						send_message(recipient_id, response_sent_nontext)
		return "Message Processed"

def varify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return "Invalid varification token"

def get_message():
	sample_responses = [
		"You are stunning!", 
		"We're proud of you.",
		"Keep on being!",
		"We're greatful to know you :)"
		]
	
	return random.choice(sample_responses)


def send_message(recipient_id, response):
	print (response, recipient_id)
	bot.send_text_message(recipient_id, response)
	return "sucess"



if __name__ == '__main__':
	# if fails, check the webhooks subscription with the ngrok
	app.run()
