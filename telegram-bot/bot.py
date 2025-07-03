import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Tu token de Telegram bot
TELEGRAM_BOT_TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"

# URL base de tu API en Render
API_BASE_URL = "https://protocolr2-bot.onrender.com"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Funciones para llamar a la API

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola Jefe! Soy el coach del Protocolo R2.\n"
        "Usa /hoy para ver la receta del día.\n"
        "Usa /estado para ver tu progreso.\n"
        "Usa /repetir para repetir el día actual.\n"
        "Usa /completar para marcar el día como completado.\n"
        "Usa /avanzar para avanzar al siguiente día.\n"
        "Usa /logros para ver tus medallas.\n"
        "Ejemplo: /dia 3 para ver el día 3."
    )

async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/hoy/{user_id}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        texto = f"{data['mensaje']}\n\n{data['contenido']}\n\n"
        # Opciones con botones para Completar o Repetir
        keyboard = [
            [
                InlineKeyboardButton("✅ Completar", callback_data="completar"),
                InlineKeyboardButton("🔁 Repetir", callback_data="repetir")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(texto, reply_markup=reply_markup)
    else:
        await update.message.reply_text("Error al obtener el día de hoy.")

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/estado/{user_id}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        texto = (
            f"📊 Estado actual:\n"
            f"Día actual: {data['Día actual']}\n"
            f"Fase: {data['Fase']}\n"
            f"Días completados: {data['Días completados']}\n"
            f"Repeticiones: {data['Repeticiones']}\n"
            f"Logros: {', '.join(data['Logros']) if data['Logros'] else 'Ninguno'}"
        )
        await update.message.reply_text(texto)
    else:
        await update.message.reply_text("Error al obtener el estado.")

async def logros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/logros/{user_id}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        texto = (
            f"🎖️ Tus logros:\n"
            f"Días completados: {data['🎖️ Días completados']}\n"
            f"Medallas: {', '.join(data['🥇 Medallas']) if data['🥇 Medallas'] else 'Ninguna'}\n"
            f"Repeticiones: {data['🔁 Repeticiones']}"
        )
        await update.message.reply_text(texto)
    else:
        await update.message.reply_text("Error al obtener los logros.")

async def dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Por favor, indica el número del día. Ejemplo: /dia 3")
        return
    try:
        n = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Número inválido. Ejemplo válido: /dia 3")
        return
    url = f"{API_BASE_URL}/dia/{n}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        await update.message.reply_text(f"Día {n}:\n\n{data['contenido']}")
    else:
        await update.message.reply_text("Día fuera de rango.")

async def repetir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/repetir/{user_id}"
    r = requests.post(url)
    if r.status_code == 200:
        data = r.json()
        await update.message.reply_text(data['mensaje'])
    else:
        await update.message.reply_text("Error al repetir el día.")

async def completar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/completar/{user_id}"
    r = requests.post(url)
    if r.status_code == 200:
        data = r.json()
        await update.message.reply_text(f"{data['mensaje']} Puntos: {data['puntos']}")
    else:
        await update.message.reply_text("Error al completar el día.")

async def avanzar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    url = f"{API_BASE_URL}/avanzar/{user_id}"
    r = requests.post(url)
    if r.status_code == 200:
        data = r.json()
        await update.message.reply_text(data['mensaje'])
    else:
        if r.status_code == 403:
            await update.message.reply_text("Primero debes completar el día actual para avanzar.")
        else:
            await update.message.reply_text("Error al avanzar de día.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "completar":
        await completar(update, context)
    elif query.data == "repetir":
        await repetir(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/hoy - Ver receta del día actual\n"
        "/estado - Ver progreso y logros\n"
        "/repetir - Repetir el día actual\n"
        "/completar - Marcar día como completado\n"
        "/avanzar - Avanzar al siguiente día\n"
        "/logros - Ver tus medallas\n"
        "/dia N - Ver contenido del día N"
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hoy", hoy))
    app.add_handler(CommandHandler("estado", estado))
    app.add_handler(CommandHandler("logros", logros))
    app.add_handler(CommandHandler("dia", dia))
    app.add_handler(CommandHandler("repetir", repetir))
    app.add_handler(CommandHandler("completar", completar))
    app.add_handler(CommandHandler("avanzar", avanzar))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot arrancando...")
    app.run_polling()

if __name__ == "__main__":
    main()
