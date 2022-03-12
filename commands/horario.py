def horario(update, context):
    update.message.reply_text(
        """ **Horario**

¡Hola! Tienes que hacer tu propio horario, la universidad solo provee los horarios y aulas de cada ramo. 
No es tan complicado, solo necesitas seguir la siguiente guía.

**[Como hacer tu propio horario](https://wiki.inf.udec.cl/doku.php?id=horario)**

*¿Tienes alguna duda o encontraste un error? Avisa al administrador.* """, parse_mode='Markdown')
