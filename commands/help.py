import logging

def help(update, context):
    logger = logging.getLogger("UdeCursosBot")
    logger.setLevel(logging.DEBUG)

    logger.info(
        f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
    )

    update.message.reply_text(
        """> *Comandos disponibles* <

• _/certs Próximos certámenes/eventos_
• _/get - Inspirational study quotes_
• _/udecursos - Lista de comandos disponibles_
• _/version - Versión del bot y código fuente_
• _/horario - Guía para crear un horario de clases_
• _/add <mes> <dia> - Añade un nuevo evento_
• _/remove - Elimina un evento_
    """, parse_mode='Markdown')
