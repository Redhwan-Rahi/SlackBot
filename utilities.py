

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

def tempMessage():
    message = {
        "blocks":[
            {
                "type":"section",
                "text":{
                    "type":"mrkdwn",
                    "text":"Hi  dsadasdsadasdasdasd:wave:"
                }
            },
        ]
    }
    return message

def errorMessage():
    msg = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Please @ the hiring leader"
                }
            }
        ]
    }
    return msg

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

# def payload():
#     res = {
# 	"type": "modal",
# 	"title": {
# 		"type": "plain_text",
# 		"text": "My App"
# 	},
# 	"submit": {
# 		"type": "plain_text",
# 		"text": "Submit"
# 	},
# 	"close": {
# 		"type": "plain_text",
# 		"text": "Cancel"
# 	},
# 	"blocks": [
# 		{
# 			"type": "input",
# 			"element": {
# 				"type": "plain_text_input",
# 				"action_id": "plain_text_input-action"
# 			},
# 			"label": {
# 				"type": "plain_text",
# 				"text": "Label"
# 			}
# 		},
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "Test block with multi static select"
# 			},
# 			"accessory": {
# 				"type": "multi_static_select",
# 				"placeholder": {
# 					"type": "plain_text",
# 					"text": "Select options"
# 				},
# 				"options": [
# 					{
# 						"text": {
# 							"type": "plain_text",
# 							"text": "*this is plain_text text*"
# 						},
# 						"value": "value-0"
# 					}
# 				],
# 				"action_id": "multi_static_select-action",
# 				"max_selected_items": 2,
                
# 			}
# 		}
# 	]
# }
#     return res
def loading():
    msg = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "My App"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": ":man-biking: Now loading..."
                }
            }
        ]
    }
    return msg

def buildList(input_arr):
    distributionLists = []
    for idx, elem in enumerate(input_arr):
        if(idx > 99):
            break
        distributionLists.append({
            "text":{
                "type":"plain_text",
                "text":"{}".format(elem['displayName'])
            },
            "value":"{}".format(elem['distinguishedName'])
        })
    return distributionLists

def payload():
    res = {
        "type": "modal",
        "callback_id":"DL",
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
                "block_id":"list_selector",
                "element": {
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select options"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":man-biking: Now loading..."
                            },
                            "value": "value-0"
                        },
                    ],
                    "action_id": "multi_static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Label"
                }
            },
            {
                "type": "input",
                "block_id":"name_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Label"
                }
            }
        ]
}
    return res


# def payload():
#     res = {
#         "type": "modal",
#         "callback_id":"distribution-list",
#         "title": {
#             "type": "plain_text",
#             "text": "My App"
#         },
#         "submit": {
#             "type": "plain_text",
#             "text": "Submit"
#         },
#         "close": {
#             "type": "plain_text",
#             "text": "Cancel"
#         },
#         "blocks": [
#             {
#                 "type": "input",
#                 "element": {
#                     "type": "plain_text_input",
#                     "action_id": "plain_text_input-action"
#                 },
#                 "label": {
#                     "type": "plain_text",
#                     "text": "Label"
#                 }
#             },
#             {
#                 "type": "input",
#                 "element": {
#                     "type": "static_select",
#                     "placeholder": {
#                         "type": "plain_text",
#                         "text": "Select an item"
#                     },
#                     "options": [
#                         {
#                             "text": {
#                                 "type": "plain_text",
#                                 "text": "*this is plain_text text*"
#                             },
#                             "value": "value-0"
#                         }
#                     ],
#                     "action_id": "static_select-action"
#                 },
#                 "label": {
#                     "type": "plain_text",
#                     "text": "Label"
#                 }
#             }
#         ]
#     }
#     return res