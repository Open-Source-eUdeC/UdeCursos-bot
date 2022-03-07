from re import A
from telegram.ext import (
    Updater,
    CommandHandler,
    StringCommandHandler
)

import os
import logging
import json
from random import randint

from components.fetch import *
from components.certs import *
from components.goodread import *
from components.formatting import Clip
from components.modify_data import *

INPUT_TEXT = 0
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
clippings = Clip()
# get = fetchToken()
token = fetchToken()
groupIDs = fetch_groups_IDs()

updater = Updater(token=fetchToken(), use_context=True)
job_queue = updater.job_queue


def start(update, context):
    update.message.reply_text(
        "👋 ¡Hey, aquí UdeCursos Bot!\n\n"
        "Todo listo para comenzar ✅\n"
        "_Para obtener ayuda escribe /udecursos_ \n\n"
        "No olvides visitarme en: [UdeCursos.study](https://udecursos.study/) 🔗 !"
    , parse_mode='Markdown')

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


def version(update, context):
    sourceCode = "https://github.com/Open-Source-eUdeC/UdeCursos-bot"
    update.message.reply_text(
        "<b>UdeCursos-bot v1.5\n</b>"
        f"<b>Código fuente: </b><a href='{sourceCode}'>GitHub</a>"
    , parse_mode="HTML")


def add_cert(update, context):
    msg = update.message.text
    usr_id = update.message.from_user.id
    chat_id = update.message.chat.id
    if user_can_modify_data(usr_id, chat_id): # User belongs to gen.superusers
        gen = get_generation(chat_id)
        args = msg.split()[1:]
        if not args_are_ok(args, "add_cert"):
            update.message.reply_text("Revisa el formato del comando con /udecursos")
            return

        cmd = "bin/insert_cert "
        cmd += gen
        for i in range(len(args)):
            cmd += " "+args[i]
        try:
            os.system(cmd)
        except:
            print("An error has occured while modifying the data :/")
            exit(1)
    else :
        update.message.reply_text(
            "Al parecer no tienes permisos para alterar los datos ¯\_(ツ)_/¯"
            "contáctate con @CxrlosKenobi"
        )



def greetThursday(context):
    with open('assets/jueves.gif', 'rb') as file:
        animated = file.read()
    for group in groupIDs:
        context.bot.send_animation(
            chat_id=group,
            animation=animated
        )


def help(update, context):
    update.message.reply_text(
        """> *Comandos disponibles* <

• _/certs Próximos certámenes/eventos_
• _/get - Inspirational study quotes_
• _/udecursos - Lista de comandos disponibles_
• _/version - Versión del bot y código fuente_
• _/schedule <nombre> <fecha> - Añade un nuevo evento_
 Ej:  _/schedule Cálculo III 2022-03-30_
    """, parse_mode='Markdown')


def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('udecursos', help))
    dp.add_handler(CommandHandler('version', version))
    dp.add_handler(CommandHandler('certs', getSubjects, pass_args=True))
    dp.add_handler(CommandHandler('schedule', add_cert))

    dp.add_handler(CommandHandler('get', get))
    job_queue = updater.job_queue
    job_queue.run_daily(
        greetThursday,
        time=dt.replace(hour=8, minute=0, second=0, microsecond=0),
        days=(3, ),
        name='Felíz Jueves'
    )


    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')
    updater.idle()

if __name__ == '__main__':
    main()
