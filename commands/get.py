from random import randint
from components.goodread import *
from components.formatting import Clip


clippings = Clip()

def get(update, context):
    seed = randint(0, len(clippings)- 1)
    highlight = clippings[seed]['highlight']
    history = push(highlight, False)

    doWhile = True
    while doWhile == True:
        if highlight in list(history.values()):
            seed = randint(0, len(clippings)- 1)
            highlight = clippings[seed]['highlight']
            doWhile = True
        elif highlight not in list(history.values()):
            source = clippings[seed]['book']
            doWhile = False
        else:
            print('\n[ * ] Cycles error at Callback')
            return exit(1)

    history = push(highlight, True)
    if len(source) < 3:
        source = clippings[seed]['author']

    update.message.reply_text(
        # chat_id=update.effective_chat.id,
        text = f'_"{highlight}"_\n- *{source}*',
        parse_mode='Markdown'
    )
