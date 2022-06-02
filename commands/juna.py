from datetime import datetime, timedelta
from components.menujunaeb import get_menu

async def juna(update, context):
  menu = get_menu()

  today = datetime.today().strftime('%d/%m/%Y')
  if datetime.now().hour >= 23: # Winter time adjustment
    today = (datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y')

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
