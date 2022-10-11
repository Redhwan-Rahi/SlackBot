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
import time
import threading
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
    print(data)
    user_id = data.get('user_id')
    user_text = data.get('text')
    channel_id = data.get('channel_id')
    messageHolder = utilities.tempMessage()
    messageHolder['blocks'] = initiateR(user_text)
    #message3 = utilities.tempMessage(user_id,user_text)
    headers = {'Authorization':f'Bearer {SLACK_BOT}', 'Content-type':'application/json'}
    response_url = data.get("response_url")
    params = {'channel':f'{channel_id}', 'blocks':json.dumps(messageHolder)}
    requests.post(response_url, data=json.dumps(messageHolder), headers=headers, verify=False)
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
    

def getResponse():
    tempArr = []
    for i in range(25):
        tempArr.append({'displayName':'US-AZ'+f'{i}', 'distinguishedName':'CN-AX-DC,=AE'+f'{i}'})
    return tempArr

def updateView(headers, params):
    time.sleep(3)
    requests.post("https://slack.com/api/views.update",headers=headers, data=params, verify=False).json()
    return

MOVIE_API_KEY = 'https://api.themoviedb.org/3/movie/upcoming?api_key=e4c0395b4795a399603e44610db36ddd'
@app.route('/movie-dl', methods=['POST'])
def movieList():
    data = request.form
    if(data.get('text')):
        user_text = data.get('text')
        if(user_text.count("@") == 1):
            if(len(user_text) > 1 and '@' in user_text):
                ads_id = (user_text.split('|')[1].strip('<>'))
                unique_id = data.get('text').split('|')[0].split('@')[1]
                print(ads_id)
            headers = {'Authorization':f'Bearer {SLACK_BOT}'}
            params = {'user':unique_id}
            modal_data = utilities.payload()
            temp_data = utilities.loading()
            params = {"trigger_id":data.get('trigger_id'), "view":json.dumps(temp_data)}
            modalPostRequest = requests.post("https://slack.com/api/views.open",headers=headers, data=params, verify=False)
            responseData = getResponse()
            response_url = data.get('response_url')
            modal_data['blocks'][0]['element']['options'] = utilities.buildList(responseData)
            modalViewId = (modalPostRequest.json().get('view')['id'])
            params = {"view_id":modalViewId, "view":json.dumps(modal_data)}
            t = threading.Thread(target=updateView, args=(headers, params))
            t.start()
            return '', 200
        else:
            return jsonify(response='error t2o'), 200
    else:
        return jsonify(response='error'), 200
    # data = request.form 
    # user_text = data.get('text')
    # print(user_text.split('|')[1].strip('<>'))
    # user_inp = user_text.split(' ')
    
    # headers = {'Authorization':f'Bearer {SLACK_BOT}'}
    # response_url = data.get('response_url')
    # if(len(user_inp) > 1):
    #     msg = utilities.errorMessage()
    #     msg['blocks'] = [{
    #             "type": "section",
    #             "text": {
    #                 "type": "plain_text",
    #                 "text": "Please try again and @ only 1 hiring leader."
    #             }
    #         }]
    #     requests.post(response_url, data=json.dumps(msg), headers=headers, verify=False)
    #     return Response(), 200
    # elif(len(user_inp) == 1 and user_inp[0] == ''):
    #     msg = utilities.errorMessage()
    #     msg['blocks'] = [{
    #             "type": "section",
    #             "text": {
    #                 "type": "plain_text",
    #                 "text": "Please try again and @ a hiring leader."
    #             }
    #         }]
    #     requests.post(response_url, data=json.dumps(msg), headers=headers, verify=False)
    #     return Response(), 200
    # else:
    #     modal_data = utilities.payload() 
    #     modal_data['blocks'][0]['element']['options'] = helper()
    #     params = {"trigger_id":data.get('trigger_id'), "view":json.dumps(modal_data)}
    #     requests.post("https://slack.com/api/views.open",headers=headers, data=params, verify=False)
        
    # return Response(), 200

INPU = []
for i in range(80):
    INPU.append({'displayName':'US-AZ'+f'{i}', 'distinguishedName':'CN=-AEXO,DC.com'+f'{i}'})

def helper():
    # response = requests.get(MOVIE_API_KEY).json()
    titles = []
    res = []
    print(INPU)
    for idx,x in enumerate(INPU):
        if(idx > 99):
            break
        res.append({
            "text":{
                "type":"plain_text",
                "text":"{}".format(x['displayName'])
            },
            "value":"{}".format(x['distinguishedName'])
        })
    return res
    # for inp in userInp:
    #     MOVIE_API_KEY2 = 'https://api.themoviedb.org/3/movie/{}?api_key=e4c0395b4795a399603e44610db36ddd'.format(inp)
    #     try:
    #         response = requests.get(MOVIE_API_KEY2).json()
    #         titles.append({
    #         "text":{
    #             "type":"plain_text",
    #             "text":"{}".format(response['title'])
    #         },
    #         "value":"{}".format("idx")
    #     })
    #     except KeyError:
    #         continue
    # return titles
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
    data_payload = json.loads(data['payload'])
    if data_payload['view']['callback_id'] == 'DL':
        obj = data_payload['view']['state']['values']
        # print(obj)
        listInput = (obj.get('list_selector').get('multi_static_select-action').get('selected_options'))
        textInput = (obj.get('name_input').get('plain_text_input-action').get('value'))
        for x in listInput:
            print(x.get('value'))
        arr = []
        for x in textInput.split(','):
            print(x)
            if(x.strip(' ').isalnum()):
                arr.append(x.strip(' '))
        print(arr)   
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

def initiateR(user_text):
    arr = []
    headers = {'Authorization':f'Bearer {SLACK_BOT}', 'Content-type':'application/json'}
    for x in (user_text.split(' ')):
        try:
            if '|' and '@' in x:
                temp = (x.split('|')[1].strip('<>'))
                iD = (x.split('|')[0].strip('@<>'))
                params = {"user":iD}
                response = requests.get('https://slack.com/api/users.info',headers=headers, data=params)
                print(response)
                print(iD, "HI")
                arr.append({
                "type":"section",
                "text":{
                    "type":"mrkdwn",
                    "text":"Hi {} :wave:".format(temp)
                }
                }
            )
        except:
            continue
    return arr

if __name__ == "__main__":
    app.run(debug=True)