from components.history import get_history
from components.fetch import get_generation

async def history(update, context):
	chat_id = update.message.chat_id
	gen = get_generation(chat_id)

	history = get_history(gen)
	body = "👁️ *Historial resumido de acciones:*\n\n"

	for item in history:
		body += f"• {item}\n"

	await update.message.reply_text(
		body,
		parse_mode='Markdown'
	)
