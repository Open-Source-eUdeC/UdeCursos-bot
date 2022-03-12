import os
import logging
import subprocess 
from pytz import timezone
from datetime import datetime
from telegram.ext import ( Updater, CommandHandler )
#
from components.fetch import fetch_token
#
from commands.start import start
from commands.help import help
from commands.version import version
from commands.certs import certs
from commands.get import get
from commands.sched import sched
from commands.sched import horario
from commands.Cronjobs import *


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initilizing config variables to be used in the bot
logger = logging.getLogger(__name__)
updater = Updater(token=fetch_token(), use_context=True)
job_queue = updater.job_queue
tz = timezone('America/Santiago')
dt = datetime.now(tz)

# Run initializer for binaries
if not os.path.exists('bin/insert_cert'):
    command = "g++ bin/src/insert_cert.cpp -o bin/insert_cert"
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('udecursos', help))
    dp.add_handler(CommandHandler('version', version))
    dp.add_handler(CommandHandler('certs', certs, pass_args=True))
    dp.add_handler(CommandHandler('sched', sched))
    dp.add_handler(CommandHandler('get', get))
    dp.add_handler(CommandHandler('horario', horario))

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
