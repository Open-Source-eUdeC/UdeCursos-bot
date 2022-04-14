from components.modify_data import *

def setAdmin(update, context):
  msg = update.message.text
  usr_id = update.message.from_user.id
  chat_id = update.message.chat.id

  if not user_can_modify_data(usr_id, chat_id): # User belongs to gen.superusers
      update.message.reply_text("Al parecer no tienes permisos para alterar los datos ¯\_(ツ)_/¯\nContáctate con @CxrlosKenobi")
      return

  args = msg.split()[1:]
  gen = get_generation(chat_id)

  print("args: ", args)
  