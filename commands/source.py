async def source(update, context):
    source_code = "https://github.com/Open-Source-eUdeC/UdeCursos-bot"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "*UdeCursos bot v2.0*\n\n"
            f"Código fuente: [GitHub]({source_code})"
        ),
        parse_mode="Markdown"
    )
