from components.modify_data import *

def setAdmin(update, context):
  msg = update.message.text
  usr_id = update.message.from_user.id
  usr_name = update.message.from_user.username
  chat_id = update.message.chat.id

  if not user_can_modify_data(usr_id, chat_id): # User belongs to gen.superusers
    update.message.reply_text("Al parecer no tienes permisos para alterar los datos ¯\_(ツ)_/¯\nContáctate con @CxrlosKenobi")
    return

  args = msg.split()[1:]
  gen = get_generation(chat_id)

  # Add the user id of args[0] to the list of superusers
  with open("data/certs.json", "r") as f:
    data = json.load(f)
  
  data[gen]["superusers"].append(int(args[0]))

  with open("data/certs.json", "w") as f:
    # Write the new data, ordered and with proper indentation
    json.dump(data, f, sort_keys=True, indent=2)
  
  update.message.reply_text(
    f"🎊 @{usr_name} ha sido añadido a la lista de superusuarios de la generación {gen}"
  )
