#REMINDER TO ALWAYS GENERATE A NEW ngrok http 5000
from re import U
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import requests

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

#client.chat_postMessage(channel='#test', text="HELLO")
BOT_ID = client.api_call('auth.test')['user_id']

message_counts = {}
ts = ''

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    ts = event.get('ts')
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if user_id != BOT_ID:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

        client.chat_postMessage(channel=channel_id, text=text)

@app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id,0)
    client.chat_postMessage(channel=channel_id, text=f"Number of Messages: {message_count}")
    return Response(), 200


@app.route('/weather', methods=['GET','POST'])
def weather():
    data = request.form
    text = data.get('text')
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="+text+"&APPID="+os.environ['WEATHER_API']
    channel_id = data.get('channel_id')
    response = requests.get(BASE_URL).json()
    tempKelvin = response['main']['temp']
    tempCelsius = tempKelvin - 273.15
    temp = tempCelsius*(9/5) + 32
    print(ts)
    client.chat_postMessage(channel=channel_id, thread_ts=ts, text=f"Weather For: {text}. Current Conditions: {response['weather'][0]['description']}. Current Temperature: {temp:.2f}")

    return Response(), 200



if __name__ == "__main__":
    app.run(debug=True)