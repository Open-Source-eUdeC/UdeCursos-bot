import logging
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
#
from components.history import save_record
from components.fetch import get_generation
from components.certs import getSubjects, cert_adder, cert_check
from commands.remove import cancel


CERT_INFO, ADD_CERT = range(2)
new_cert = {}
gen = None

async def add(update, context):
    logger = logging.getLogger("UdeCursosBot")
    logger.setLevel(logging.DEBUG)
    logger.info(
        f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
    )

    chat_id = update.message.chat_id
    global gen
    gen = get_generation(chat_id)

    try:
        args = update.message.text.split()[1].split('-')
        if (
            (len(args) != 2) or 
            not (0 < int(args[1]) <= 31) or 
            not (0 < int(args[0]) <= 12)
        ):
            await update.message.reply_text(
                """
                🙁 *¡Formato de fecha inválido!*
                \n_Ejemplo: /add MM-DD_
                """,
                parse_mode='Markdown'
            ); return ConversationHandler.END

    except Exception as e:
        print(e)
        await update.message.reply_text(
            """
            🙁 *¡Formato de fecha inválido!*
            \n_Ejemplo: /add MM-DD_
            """,
            parse_mode='Markdown'
        ); return ConversationHandler.END

    new_cert["date"] = f"{datetime.now().year}-{args[0]}-{args[1]}"

    reply_keyboard = [[sub] for sub in getSubjects(gen)]
    reply_keyboard.append(["✍️ Otro (ingresar manualmente)"])

    await update.message.reply_text(
        f"""
        _Fecha de evaluación registrada: {new_cert["date"]}_
        \n*Selecciona la asignatura a evaluar: ⬇️*
        """,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="/cancel para abortar",
            one_time_keyboard=True,
            resize_keyboard=True,
            selective=True
        )

    ); return CERT_INFO

async def cert_info(update, context):
    if update.message.text == "/cancel":
        await cancel(update, context)
        return ConversationHandler.END

    if ("Otro" in update.message.text):
        await update.message.reply_text(
            """
            *Ingresa el nombre de la asignatura: ⬇️*
            """,
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        ); return CERT_INFO

    new_cert["name"] = update.message.text

    await update.message.reply_text(
        """
        *Elige el tipo de evaluación: ⬇️*
        """,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardMarkup(
            [['Cert', 'Test', 'Tarea']],
            input_field_placeholder="/cancel para abortar",
            one_time_keyboard=True,
            resize_keyboard=True,
            selective=True
        )
    ); return ADD_CERT

async def cert_operation(update, context):
    logger = logging.getLogger("UdeCursosBot")
    logger.setLevel(logging.DEBUG)

    new_cert["type"] = update.message.text
    try:
        cert = {'date': new_cert['date'], 'type': new_cert['type'], 'name': new_cert['name']}

        if cert_check(cert, gen):
            await update.message.reply_text(
                """
                🙁 *La evaluación que intentas agregar ya está registrada.*
                """,
                parse_mode='Markdown'
            ); return ConversationHandler.END
        else:
            cert_adder(cert, gen)
            usr_id = update.message.from_user.id
            usr_name = update.message.from_user.first_name
            params = [new_cert['date'], new_cert['type'], new_cert['name']]
            save_record(gen, '/add', params, usr_name, usr_id)

    except Exception as e:
      print(e)
      await update.message.reply_text(
          """
          🙁 ¡Hubo un error inesperado al agregar la evaluación!
          \nConsulta a un administrador para que revise el registro o intenta de nuevo.
          """,
          parse_mode='Markdown'
      ); return ConversationHandler.END 

    logger.info(
        f"{update.message.text} -> Added {new_cert['name']} {new_cert['type']} {new_cert['date']} at ({update.message.chat.title})"
    )
    await update.message.reply_text(
        f"""
        *🎉 ¡La fecha de evaluación ha sido agregada!.*
        """,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
