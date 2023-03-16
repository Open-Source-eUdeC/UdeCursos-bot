import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters
)
#
from components.fetch import fetch_token
from commands.source import source
from commands.getid import getID, getGroupID
from commands.history import history
from commands.certs import certs
from commands.juna import juna
from commands.remove import *
from commands.add import *

logger = logging.getLogger("UdeCursosBot")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - (%(name)s) - [%(levelname)s] -- %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logging.basicConfig(
    filename="logs/console.log", 
    format="%(asctime)s - (%(name)s) - [%(levelname)s] -- %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
)

async def start(update: Update, context: CallbackContext):
    logger.info(
        f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) started the bot"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "👋 ¡Hey, aquí UdeCursos Bot!\n\n"
            "Todo listo para comenzar ✅\n"
            "_Para obtener ayuda escribe /udecursos_ \n\n"
            "No olvides visitarme en: [UdeCursos.study](https://udecursos.study/) 🔗 !"
        ),
        parse_mode='Markdown'
    )


if __name__ == "__main__":
    logger.info("Starting bot...")
    bot = (
        ApplicationBuilder()
        .token(fetch_token())
        .build()
    )

    logger.info("Adding handlers...")
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("source", source))
    bot.add_handler(CommandHandler("myid", getID))
    bot.add_handler(CommandHandler("groupid", getGroupID))
    bot.add_handler(CommandHandler("certs", certs))
    bot.add_handler(CommandHandler("history", history))
    bot.add_handler(CommandHandler("juna", juna))

    add_conv = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            CERT_INFO: [MessageHandler(filters.TEXT, cert_info)],
            ADD_CERT: [MessageHandler(filters.TEXT, cert_operation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    remove_conv = ConversationHandler(
        entry_points=[CommandHandler('remove', remove)],
        states={
            REMOVE_CONFIRM: [MessageHandler(filters.TEXT, remove_confirm)], # Pending Regex filter
            REMOVE_CERT: [MessageHandler(filters.Regex("^(👍|❌)$"), remove_cert)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    bot.add_handler(add_conv)
    bot.add_handler(remove_conv)

    logger.info("Starting polling...")
    bot.run_polling()
