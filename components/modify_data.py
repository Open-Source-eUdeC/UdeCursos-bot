from telegram import Chat
import requests
import json
from components.fetch import *

def get_admins(chat_id):
    f = fetchToken()
    url = 'https://api.telegram.org/bot'
    url += f['token']
    url += '/getChatAdministrators'
    url += '?chat_id='
    url += str(chat_id)
    print(url)
    r = requests.get(url)
    print(r)
    return r.text

def get_users_able_to_modify(chat_id):
    file_location = 'data'+str(chat_id)+'.txt'
    with open(file_location) as f:
        print(f)

def user_can_modify_data(user_id, chat_id):
    # chat = Chat(group_id, 'group')
    # print(chat.get_administrators())
    admins = get_users_able_to_modify(chat_id)
    # admins = get_admins(chat_id)
    # print(admins)
