from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from datetime import datetime
import pytz
import json
from random import randint

tz = pytz.timezone('America/Santiago')
dt = datetime.now(tz)

with open('data.json', 'r') as file:
    data = json.load(file)


def push(highlight, verified):
    if verified is True:
        with open('data/records.json', 'r') as file:
            hist = json.load(file)
            # Check efficiency for this sort later
            hist['0'] = hist['1']
            hist['1'] = hist['2']
            hist['2'] = hist['3']
            hist['3'] = hist['4']
            hist['4'] = hist['5']
            hist['5'] = hist['6']
            hist['6'] = hist['7']
            hist['7'] = hist['8']
            hist['8'] = hist['9']
            hist['9'] = hist['10']
            hist['10'] = highlight
            with open('data/records.json', 'w') as file:
                json.dump(hist, file, indent=4)
    else:
        with open('data/records.json', 'r') as file:
            hist = json.load(file)
            return hist

def btnMode(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Morning Mode', callback_data='morning')],
            [InlineKeyboardButton(text='Noon Mode', callback_data='noon')],
            [InlineKeyboardButton(text='Night Mode', callback_data='night')]
        ])
    )


def morningMode():
    h = randint(7, 11)
    m = randint(0, 60)

    name = 'Have a good read at morning!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=0, microsecond=0)
    
    return time, days, name

def noonMode():
    h = randint(13, 18)
    m = randint(0, 60)

    name = 'Have a good read at noon!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=00, microsecond=0)

    return time, days, name

def nightMode():
    h = randint(20, 22)
    m = randint(0, 60)

    name = 'Have a good read at night!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=0, microsecond=0)

    return time, days, name

