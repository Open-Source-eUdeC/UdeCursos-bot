import logging
#
from components.history import get_history
from components.fetch import get_generation

async def history(update, context):
	logger = logging.getLogger("UdeCursosBot")
	logger.setLevel(logging.DEBUG)

	logger.info(
		f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
	)
	chat_id = update.message.chat_id
	gen = get_generation(chat_id)

	history = get_history(gen)
	body = "👁️ *Historial resumido de acciones:*\n\n"

	for item in history:
		body += f"• {item}\n"

	logger.info(
		f"{update.message.text} -> replied at ({update.message.chat.title})"
	)

	await update.message.reply_text(
		body,
		parse_mode='Markdown'
	)
