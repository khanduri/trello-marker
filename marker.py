import requests
import json
import os


KEY = os.environ['TRELLO_KEY']
TOKEN = os.environ['TRELLO_TOKEN']

BOARD_ID_BACKLOG = os.environ['BOARD_ID']

lists_url = "https://api.trello.com/1/boards/{}/lists?".format(BOARD_ID_BACKLOG)
response = requests.request("GET", lists_url + '&key={}&token={}'.format(KEY, TOKEN))
lists = json.loads(response.text)

name_mappings = {
    'Immediate': 'red',
    'Small': 'green',
    'Medium': 'yellow',
    'Large': 'orange',
}

for current_list in lists:
    print('====')
    current_name = current_list['name']

    colour = None
    for name in name_mappings:
        if name in current_name:
            colour = name_mappings[name]

    if not colour:
        print("---- NOTE: Colour not found for name: {}".format(current_name))
        continue

    print("starting: -- {}".format(current_name))

    list_id = current_list['id']

    url = "https://api.trello.com/1/lists/{}/cards/?".format(list_id)
    print(url)
    response = requests.request("GET", url + '&key={}&token={}'.format(KEY, TOKEN))
    cards = json.loads(response.text)

    for card in cards:
        url = "https://api.trello.com/1/cards/{}/labels/?".format(card['id'])
        querystring = {"color": colour}
        print(url)
        requests.request("POST",  url + '&key={}&token={}'.format(KEY, TOKEN), params=querystring)

    print("complete: -- {}".format(current_name))
    print('====')

