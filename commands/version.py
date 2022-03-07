def version(update, context):
    sourceCode = "https://github.com/Open-Source-eUdeC/UdeCursos-bot"
    update.message.reply_text(
        "<b>UdeCursos-bot v1.5\n</b>"
        f"<b>Código fuente: </b><a href='{sourceCode}'>GitHub</a>"
    , parse_mode="HTML")
