from telegram import Chat
import requests
import json
from components.fetch import *


def get_users_able_to_modify(chat_id):
    chat_id = str(chat_id)
    data = get_certs_data()
    gen = get_generation(chat_id)
    return data[gen]["superusers"]


def user_can_modify_data(user_id, chat_id):
    superusers = get_users_able_to_modify(chat_id)
    return user_id in superusers

def args_are_ok(args, command):
    if command == "add_cert":
        date = args[-1].split("-")
        if len(date) != 3:
            return False
        if len(date[0]) != 4:
            return False
        try :
            y = int(date[0]) # Year
            m = int(date[1]) # Month
            d = int(date[2]) # Day
        except:
            return False 

        if d > 31 or m > 12:
            return False

        return True