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
from commands.remove import *
from commands.add import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
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
    bot = (
        ApplicationBuilder()
        .token(fetch_token())
        .build()
    )

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("source", source))
    bot.add_handler(CommandHandler("myid", getID))
    bot.add_handler(CommandHandler("groupid", getGroupID))
    bot.add_handler(CommandHandler("certs", certs))
    bot.add_handler(CommandHandler("history", history))

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

    bot.run_polling()
