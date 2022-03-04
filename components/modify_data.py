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
