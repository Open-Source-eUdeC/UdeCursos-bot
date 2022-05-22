import json
#
from components.fetch import get_generation
from components.certs import getRemainingDays


async def certs(update, context):
    with open('data/certs.json') as file:
        data = json.load(file)

    alertMsg = """
⚠️ ¡Asegúrate de seguir el formato!
      _/certs <rango> <ramoI, ramoII ...>_
"""
    noneMsg = """
🙁 ¡Oops! No poseo asignaturas o eventos así hasta la fecha.
"""
    try:
        if context.args[0] == 'help':
            await update.message.reply_text(alertMsg, parse_mode='Markdown')
            return
    except IndexError:
        print('[ ! ] No arguments were given')
        pass

    try:
        rango = int(context.args[0])
        if rango > 120: rango = 120
    except (IndexError, ValueError):
        rango = 45
    
    try:
        if not (context.args[0].isdigit()):
            ramosRaw = context.args

        elif (context.args[0].isdigit()):
            if len(context.args) > 1:
                ramosRaw = context.args[1:]
            elif len(context.args) == 1:
                ramosRaw = []
        else:
            await update.message.reply_text(alertMsg, parse_mode='Markdown')
            return
    except IndexError:
        print('[ ! ] No arguments were given')
        ramosRaw = []
    
    ramos = []
    for j in ramosRaw:
        try:
            if (j[-1] == 'I') and (j[-2] == 'I'):
                j = j.replace('II', ' II')
                ramos.append(j.lower())
            elif (j[-1] == 'I') and (j[-2] != 'I'):
                j = j.replace('I', ' I')
                ramos.append(j.lower())

            elif (j[-1] == 'i') and (j[-2] == 'i'):
                j = j.replace('ii', ' ii')
                ramos.append(j.lower())
            elif (j[-1] == 'i') and (j[-2] != 'i'):
                j = j.replace('i', ' i')
                ramos.append(j.lower())
            else:
                ramos.append(j.lower())
                pass
        except IndexError:
            ramos.append(j.lower())
            pass

    chat_id = str(update.message.chat_id)
    gen = get_generation(chat_id)

    if gen == None:
        await update.message.reply_text(
            """
            🙁 ¡No puedo obtener tu generación de la base de datos!
            \nConsulta a un administrador para que realice el registro.
            """,
            parse_mode='Markdown'
        ); return
    
    subjectsList = []
    for subject in data[gen]['certs']:
        if getRemainingDays(subject) > rango:
            continue
        if ramos:
            if subject['name'].lower() in ramos:
                subjectsList.append(f"{getRemainingDays(subject)} días - {subject['name']}")
            else:
                continue
        else:
            subjectsList.append(f"{getRemainingDays(subject)} días ({subject['type']})\n{subject['name']}\n")
    if subjectsList == []:
        await update.message.reply_text(noneMsg, parse_mode='Markdown')
        return
    else:
        subjectsList.sort(key=lambda x: int(x.split(' ')[0]))



    body = f"""
    ✳️ *Próximas Evaluaciones* ✳️
~ Rango: {rango} días

"""

    status = ['🏳', '🔴', '🟠', '🟡', '🟢', 'DONE']
    for subject in subjectsList:
        remaining = int(subject.split(' ')[0])
        if remaining < 0:
            continue
        elif 0 <= remaining <= 2:
            assignedStatus = status[0]
        elif 3 <= remaining <= 7 :
            assignedStatus = status[1]
        elif 8 <= remaining <= 14:
            assignedStatus = status[2]
        elif 15 <= remaining <= 23:
            assignedStatus = status[3]
        else:
            assignedStatus = status[4]

        body += f"• {assignedStatus} _{subject}_\n"

    await update.message.reply_text(body, parse_mode='Markdown')
