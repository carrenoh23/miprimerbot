# -*- coding: utf-8 -*-

# Importamos las clases necesarias de la librería python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import random 
import os # ¡NUEVA LÍNEA: Importamos el módulo os para variables de entorno!

# --- Variables de Configuración (Ahora desde Variables de Entorno) ---
# Obtiene el token del bot de una variable de entorno llamada TELEGRAM_BOT_TOKEN
token = os.getenv("TELEGRAM_BOT_TOKEN") 
# Obtiene el ID del canal de una variable de entorno llamada TELEGRAM_CANAL_ID
CANAL_ID = os.getenv("TELEGRAM_CANAL_ID") 

# --- ¡IMPORTANTE! Verificación para asegurar que las variables se cargaron ---
if not token or not CANAL_ID:
    print("ERROR: Las variables de entorno TELEGRAM_BOT_TOKEN o TELEGRAM_CANAL_ID no están configuradas.")
    print("Asegúrate de haberlas establecido en Render.com.")
    # Exit(1) hace que el script termine si no se encuentran las variables,
    # lo cual es bueno para evitar que el bot intente iniciarse sin credenciales.
    exit(1) 
# ----------------------------------------------------------------------


# --- Funciones de tu bot ---

# Función para el comando /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot. ¡Listo para ayudarte!')

# Función para el comando /help (actualizada con todas las funcionalidades)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = """Aquí están los comandos que conozco:
/start - Inicia una conversación con el bot y te saluda.
/help - Muestra esta lista de comandos.
/datodeldia - Muestra un dato interesante o una frase inspiradora.
(Reenvíame cualquier mensaje en privado para publicarlo en el canal.)
(También puedes enviarme un mensaje de texto normal en privado para publicarlo.)
"""
    await update.message.reply_text(help_message)

# Función para el comando /datodeldia con lista de frases aleatorias
async def datodeldia_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    frases_motivadoras = [
        "La única forma de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
        "El éxito es la suma de pequeños esfuerzos repetidos día tras día. - Robert Collier",
        "No te rindas, la vida es eso, continuar el viaje, perseguir tus sueños. - Mario Benedetti",
        "Haz de cada día tu obra maestra. - John Wooden",
        "La vida es un 10% lo que te pasa y un 90% cómo reaccionas a ello. - Charles R. Swindoll",
        "Sé el cambio que quieres ver en el mundo. - Mahatma Gandhi",
        "El futuro pertenece a quienes creen en la belleza de sus sueños. - Eleanor Roosevelt",
        "La felicidad no es algo ya hecho. Viene de tus propias acciones. - Dalai Lama",
        "Nunca es demasiado tarde para ser lo que podrías haber sido. - George Eliot",
        "Lo que la mente del hombre puede concebir y creer, la mente del hombre puede lograr. - Napoleon Hill",
        "Cree que puedes y ya estarás a medio camino. - Theodore Roosevelt",
        "La mejor venganza es un éxito masivo. - Frank Sinatra",
        "No cuentes los días, haz que los días cuenten. - Muhammad Ali",
        "Si puedes soñarlo, puedes lograrlo. - Zig Ziglar",
        "La acción es la clave fundamental para todo éxito. - Pablo Picasso"
    ]
    
    frase_aleatoria = random.choice(frases_motivadoras)
    
    # El bot responderá con la frase elegida al azar en el chat donde se envió el comando.
    await update.message.reply_text(frase_aleatoria)
    
    # El bot también envía la misma frase a tu canal
    await context.bot.send_message(chat_id=CANAL_ID, text=frase_aleatoria)
    
# --- Función para reenviar cualquier mensaje de texto PRIVADO (no comando, no forward) al canal ---
async def reenviar_texto_a_canal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == "private":
        mensaje_original = update.message.text 
        try:
            await context.bot.send_message(chat_id=CANAL_ID, text=mensaje_original)
            await update.message.reply_text("Mensaje de texto reenviado al canal correctamente.")
        except Exception as e:
            await update.message.reply_text(f"Error al reenviar el mensaje de texto al canal: {e}")
    else:
        pass 

# --- Función para reenviar mensajes FORWARDED (de otros canales/chats) al canal ---
async def reenviar_externo_a_canal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == "private" and update.message.forward_origin:
        try:
            await context.bot.forward_message(
                chat_id=CANAL_ID,
                from_chat_id=update.message.chat_id, 
                message_id=update.message.message_id 
            )
            await update.message.reply_text("Mensaje reenviado a tu canal desde la fuente original.")
        except Exception as e:
            await update.message.reply_text(f"Error al reenviar el mensaje externo al canal: {e}")
    else:
        pass 

# --- Función Principal para Configurar y Arrancar el Bot ---

def main() -> None:
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("datodeldia", datodeldia_command))

    application.add_handler(MessageHandler(filters.FORWARDED, reenviar_externo_a_canal))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reenviar_texto_a_canal))


    print("El bot está arrancando...")
    application.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()