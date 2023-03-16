import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
#
from components.fetch import get_generation
from components.history import save_record
from components.certs import getCerts, cert_remover

REMOVE_CONFIRM, REMOVE_CERT = range(2)
chosen_cert = None
gen = None

async def remove(update, context):
  logger = logging.getLogger("UdeCursosBot")
  logger.setLevel(logging.DEBUG)

  logger.info(
      f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
  )

  chat_id = update.message.chat_id
  global gen
  gen = get_generation(chat_id)

  reply_keyboard = []
  for sub in getCerts(update, gen):
    reply_keyboard.append([f"[{sub['type']}] {sub['name']} {sub['date']}"])

  if len(reply_keyboard) == 0:
    await update.message.reply_text(
        """
        🙁 *¡No hay fechas de evaluación para remover!*
        \nRecuerda que puedes agregar fechas de evaluación con el comando _/add_.
        """,
        parse_mode='Markdown'
    ); return ConversationHandler.END

  await update.message.reply_text(
      """
      *Elige una evaluación de la lista para eliminar:*
      """,
      parse_mode='Markdown',
      reply_markup=ReplyKeyboardMarkup(
        reply_keyboard,
        input_field_placeholder="/cancel para abortar",
        one_time_keyboard=True,
        resize_keyboard=True,
        selective=True
      )
  )

  return REMOVE_CONFIRM


async def remove_confirm(update, context):
  global chosen_cert
  chosen_cert = update.message.text

  if chosen_cert == "/cancel":
    await cancel(update, context)
    return ConversationHandler.END

  await update.message.reply_text(
      f"""
      *¿Estás seguro de querer eliminar esta evaluación?:*
      \n*- {chosen_cert}*
      """,
      parse_mode='Markdown',
      reply_markup=ReplyKeyboardMarkup(
        [['👍', '❌']],
        input_field_placeholder="/cancel para abortar",
        one_time_keyboard=True,
        resize_keyboard=True,
        selective=True
      )
  )

  return REMOVE_CERT
    

async def remove_cert(update, context):
  logger = logging.getLogger("UdeCursosBot")
  logger.setLevel(logging.DEBUG)
  response = update.message.text
  
  if response == '👍':
    logger.info(
      f"{update.message.text} -> removed {chosen_cert} at ({update.message.chat.title})"
    )

    try:
      cert_remover(chosen_cert, gen)
      usr_id = update.message.from_user.id
      usr_name = update.message.from_user.first_name
      params = [chosen_cert]
      save_record(gen, '/remove', params, usr_name, usr_id)

    except Exception as e:
      print(e)
      await update.message.reply_text(
          """
          🙁 ¡Hubo un error inesperado al eliminar la evaluación!
          \nConsulta a un administrador para que revise el registro o intenta de nuevo.
          """,
          parse_mode='Markdown'
      ); return ConversationHandler.END

    await update.message.reply_text(
        f"""
        *🗑️ La fecha de evaluación ha sido removida.*
        """,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    ); return ConversationHandler.END

  elif response == '❌':
    logger.info(
      f"{update.message.text} -> canceled removal of {chosen_cert} at ({update.message.chat.title})"
    )

    await update.message.reply_text(
        """
        *⚠️ La operación ha sido cancelada.*
        """,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    ); return ConversationHandler.END


async def cancel(update, context):
  await update.message.reply_text(
      """
      *⚠️ La operación ha sido cancelada.*
      """,
      parse_mode='Markdown',
      reply_markup=ReplyKeyboardRemove()
  ); return ConversationHandler.END
