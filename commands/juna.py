import logging
from datetime import datetime, timedelta
from components.menujunaeb import get_menu

async def juna(update, context):
  logger = logging.getLogger("UdeCursosBot")
  logger.setLevel(logging.DEBUG)

  logger.info(
    f"{update.message.text} <- User @{update.effective_user.username} ({update.effective_user.first_name}) requested"
  )

  menu = get_menu()

  today = datetime.today().strftime('%d/%m/%Y')
  if datetime.now().hour >= 23: # Winter time adjustment
    today = (datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y')

  logger.info(
    f"{update.message.text} -> replied at ({update.message.chat.title})"
  )

  await update.message.reply_text(
    f"""
    🦆 *Menu Los Patos* 🦆\n~ _{today}_
    \n- *Sopa/Ensalada*: \n_{menu["Sopa/Ensalada"]}_
    \n- *Alternativa I*: \n_{menu['Alternativa I']}_
    \n- *Alternativa II*: \n_{menu['Alternativa II']}_
    \n- *Postre I*: \n_{menu['Postre I']}_
    \n- *Postre II*: \n_{menu['Postre II']}_
    """,
    parse_mode='Markdown'
  )
