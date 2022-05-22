from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
#
from components.modify_data import user_can_modify_data
from components.fetch import get_generation
from components.certs import getSubjectsList, subject_remover

REMOVE_CERT, OPERATION = range(2)
chosen_cert = None
gen = None

async def remove(update, context):
  usr_id = update.message.from_user.id
  chat_id = update.message.chat_id
  global gen
  gen = get_generation(chat_id)

  if not user_can_modify_data(usr_id, chat_id):
    await update.message.reply_text(
        """
        🚫 *¡No tienes permisos para modificar los datos!*
        \nConsulta con un administrador para obtener permisos.            
        """,
        parse_mode='Markdown'
    ); return

  reply_keyboard = []
  for sub in getSubjectsList(update, gen):
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

  return REMOVE_CERT


async def remove_cert(update, context):
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

  return OPERATION
    

async def operation(update, context):
  response = update.message.text
  
  if response == '👍':
    try:
      subject_remover(chosen_cert, gen)
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
    )
    return ConversationHandler.END

  elif response == '❌':
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
