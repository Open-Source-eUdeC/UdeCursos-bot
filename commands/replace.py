from components.modify_data import * 


def sched(update, context):
    msg = update.message.text
    usr_id = update.message.from_user.id
    chat_id = update.message.chat.id
    
    if not user_can_modify_data(usr_id, chat_id): # User belongs to gen.superusers
        update.message.reply_text("Al parecer no tienes permisos para alterar los datos ¯-_(ツ)_-¯\nContáctate con @CxrlosKenobi")
        return

    args = msg.split()[1:]
    action = args[0]
    args = args[1:]
    gen = get_generation(chat_id)

    if action == "replace":
        if not args_are_ok(args, "replace_cert"):
            update.message.reply_text("Revisa el formato del comando con /udecursos")
            return
        
        update.message.reply_text(
            replace_cert(args, usr_id, chat_id, gen),
            parse_mode='Markdown'
        )
        return
