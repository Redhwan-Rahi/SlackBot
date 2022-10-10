invalid_users = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type":"markdown",
                "text":"HELLO YADDA YADDA"
            }
        }
    ]
}

def tempMessage(user_id, user_text):
    message = {
        "blocks":[
            {
                "type":"section",
                "text":{
                    "type":"mrkdwn",
                    "text":"Hi {} dsadasdsadasdasdasd:wave:".format(user_id)
                }
            },
            {
                "type":"section",
                "text":{
                    "type":"mrkdwn",
                    "text":"Everything you typed: {}".format(user_text)
                }
            }
        ]
    }
    return message

def tempMessage1(user_id):
    message1 = [
        {
            "type":"section",
            "text":{
                "type":"mrkdwn",
                "text":"Hi {} dasdadasd".format(user_id)
            }
        }
    ]
    return message1

def payload():
    res = {
        "type": "modal",
        "callback_id":"distribution-list",
        "title": {
            "type": "plain_text",
            "text": "My App"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Label"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*"
                            },
                            "value": "value-0"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Label"
                }
            }
        ]
    }
    return res