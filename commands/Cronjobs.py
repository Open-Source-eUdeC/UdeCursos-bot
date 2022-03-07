
from components.fetch import fetch_groups_IDs


groupIDs = fetch_groups_IDs()

def greetThursday(context):
    with open('assets/jueves.gif', 'rb') as file:
        animated = file.read()
    for group in groupIDs:
        context.bot.send_animation(
            chat_id=group,
            animation=animated
        )
