def help(update, context):
    update.message.reply_text(
        """> *Comandos disponibles* <

• _/certs Próximos certámenes/eventos_
• _/get - Inspirational study quotes_
• _/udecursos - Lista de comandos disponibles_
• _/version - Versión del bot y código fuente_
• _/horario - Guía para crear un horario de clases_
• _/sched <acción> <tipo> <nombre> [<fecha>] - Añade un nuevo evento_
    acciones: add
 Ej:  _/sched add Test Cálculo III 2022-03-30_
      _/sched add Cert Álgebra I 2022-09-01_
    """, parse_mode='Markdown')
