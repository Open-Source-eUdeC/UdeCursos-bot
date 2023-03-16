import logging

async def getID(update, context):
  logger = logging.getLogger("UdeCursosBot")
  logger.setLevel(logging.DEBUG)

  logger.info(
    f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
  )
  logger.info(
    f"{update.message.text} -> replied at ({update.message.chat.title})"
  )

  # Return the ID of the user that sent the message
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"*Tu ID es: *{update.effective_user.id}",
    parse_mode="Markdown"
  )

async def getGroupID(update, context):
  logger = logging.getLogger("UdeCursosBot")
  logger.setLevel(logging.DEBUG)

  logger.info(
    f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
  )
  logger.info(
    f"{update.message.text} -> replied at ({update.message.chat.title})"
  )

  # Return the ID of the group from which the message was sent
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"*El ID del grupo es: *{update.effective_chat.id}",
    parse_mode="Markdown"
  )
