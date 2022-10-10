#REMINDER TO ALWAYS GENERATE A NEW ngrok http 5000
import logging
from re import U
from tkinter import dialog
from urllib import response
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response, jsonify
from slackeventsapi import SlackEventAdapter
import requests
import utilities
import json

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
SLACK_BOT = token=os.environ['SLACK_TOKEN']
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
    user_text = data.get('text')
    channel_id = data.get('channel_id')   
    message3 = utilities.tempMessage(user_id,user_text)
    headers = {'Authorization':f'Bearer {SLACK_BOT}', 'Content-type':'application/json'}
    response_url = data.get("response_url")
    params = {'channel':f'{channel_id}', 'blocks':json.dumps(message3)}
    requests.post(response_url, data=json.dumps(message3), headers=headers, verify=False)
    return Response(), 200

@app.route('/weather', methods=['GET','POST'])
def weather():
    data = request.form
    print(data)
    text = data.get('text')
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="+text+"&APPID="+os.environ['WEATHER_API']
    channel_id = data.get('channel_id')
    response = requests.get(BASE_URL).json()
    client.chat_postMessage(channel=channel_id, text=response)
    tempKelvin = response['main']['temp']
    tempCelsius = tempKelvin - 273.15
    temp = tempCelsius*(9/5) + 32
    print(ts)
    # client.chat_postMessage(channel=channel_id, thread_ts=ts, text=f"Weather For: {text}. \nCurrent Conditions: {response['weather'][0]['description']}. \nCurrent Temperature: {temp:.2f}°F")
    return Response(data.to_dict), 200
    
MOVIE_API_KEY = 'https://api.themoviedb.org/3/movie/upcoming?api_key=e4c0395b4795a399603e44610db36ddd'
@app.route('/movie-dl', methods=['POST'])
def movieList():
    data = request.form 
    user_text = data.get('text')
    userInp = [x.strip() for x in user_text.split(',')]   
    modal_data = utilities.payload() 
    modal_data['blocks'][1]['element']['options'] = helper(userInp)
    headers = {'Authorization':f'Bearer {SLACK_BOT}'}
    params = {"trigger_id":data.get('trigger_id'), "view":json.dumps(modal_data)}
    requests.post("https://slack.com/api/views.open",headers=headers, data=params, verify=False)
    
    return Response(), 200

def helper(userInp):
    # response = requests.get(MOVIE_API_KEY).json()
    titles = []
    for inp in userInp:
        MOVIE_API_KEY2 = 'https://api.themoviedb.org/3/movie/{}?api_key=e4c0395b4795a399603e44610db36ddd'.format(inp)
        try:
            response = requests.get(MOVIE_API_KEY2).json()
            titles.append({
            "text":{
                "type":"plain_text",
                "text":"{}".format(response['title'])
            },
            "value":"{}".format("idx")
        })
        except KeyError:
            continue
    return titles
    # titles = []
    # for idx, x in enumerate(response.get('results')):
    #     titles.append({
    #         "text":{
    #             "type":"plain_text",
    #             "text":"{}".format(x['title'])
    #         },
    #         "value":"{}".format(idx)
    #     })
    # return titles
    

@app.route('/interaction', methods=['POST','GET','PUT'])
def receive():
    data = request.form.to_dict()
    print(data)
    data_payload = json.loads(data['payload'])
    if data_payload['view']['callback_id'] == 'distribution-list':
        print("HELLO WORLD")   
    return Response(), 201

@app.route('/preboard-dl', methods=['POST','GET','PUT'])
def preboard():
    data = request.form
    user_text = data.get('text')
    inpText = [x.strip() for x in user_text.split(',')]
    for text in inpText:
        if(text.isupper()):
            print(text)

    # arr = []
    # response = requests.get(MOVIE_API_KEY).json()
    
    # for x in response.get("results"):
    #     print(x['title'])
    #     arr.append(x['title'])



    # counter = 1
    # NEW_RESULTS = True
    # titles = []
    # while(NEW_RESULTS):
    #     URL = ('https://api.themoviedb.org/3/movie/upcoming?api_key=e4c0395b4795a399603e44610db36ddd&page='+f'{counter}')
    #     response = requests.get(URL).json()
    #     NEW_RESULTS = response.get("results",[])
    #     for idx in response.get('results'):
    #         titles.append(idx['title'])
    #     counter += 1
    # print(titles)

    headers = {'Authorization':f'Bearer {SLACK_BOT}', 'Content-type':'application/json'}
    response_url = data.get("response_url")
    user_id = data.get('user_id')
    message3 = utilities.tempMessage(user_id,user_text)
    requests.post(response_url, data=json.dumps(message3), headers=headers, verify=False)

    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)