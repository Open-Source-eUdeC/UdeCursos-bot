from telegram import Chat
import os
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

    if command == "del_cert":
        return True

def add_cert(args, usr_id, chat_id, gen):
    cmd = "bin/insert_cert "
    cmd += f"{gen} {args[0]}"

    for i in range(1, len(args)):
        cmd += " " + args[i]
    try:
        os.system(cmd)
        return "🎉 ¡Evaluación añadida!"
    except:
        print("An error has occured while modifying the data :/")
        exit(1)

def del_cert(args, usr_id, chat_id, gen):
    pass
