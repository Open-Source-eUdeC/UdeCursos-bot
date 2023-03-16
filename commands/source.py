import logging

async def source(update, context):
    logger = logging.getLogger("UdeCursosBot")
    logger.setLevel(logging.DEBUG)
    logger.info(
        f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
    )

    source_code = "https://github.com/Open-Source-eUdeC/UdeCursos-bot"

    logger.info(
        f"{update.message.text} -> replied at ({update.message.chat.title})"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "*UdeCursos bot v2.0*\n\n"
            f"Código fuente: [GitHub]({source_code})"
        ),
        parse_mode="Markdown"
    )
