import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"
BACKEND_URL = "https://protocolr2-backend.onrender.com"

logging.basicConfig(level=logging.INFO)

# Definimos teclado con botones
keyboard = [
    [KeyboardButton("📅 Hoy"), KeyboardButton("📊 Estado")],
    [KeyboardButton("✅ Completar"), KeyboardButton("🔁 Repetir")],
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    requests.get(f"{BACKEND_URL}/estado/{user_id}")  # Inicializa usuario en backend
    await update.message.reply_text(
        "👋 ¡Bienvenido al Protocolo R2!\nUsá los botones para navegar.",
        reply_markup=markup
    )


# Funciones que responden a botones
async def manejar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    user_id = str(update.effective_user.id)

    if texto == "📅 Hoy":
        r = requests.get(f"{BACKEND_URL}/hoy/{user_id}")
        if r.ok:
            data = r.json()
            await update.message.reply_text(f"{data['mensaje']}\n\n{data['contenido']}")
        else:
            await update.message.reply_text("Error al obtener el contenido de hoy.")

    elif texto == "📊 Estado":
        r = requests.get(f"{BACKEND_URL}/estado/{user_id}")
        if r.ok:
            data = r.json()
            texto_estado = (
                f"📅 Día actual: {data['Día actual']}\n"
                f"🌀 Fase: {data['Fase']}\n"
                f"✅ Días completados: {data['Días completados']}\n"
                f"🔁 Repeticiones: {data['Repeticiones']}\n"
                f"🏅 Logros: {', '.join(data['Logros']) if data['Logros'] else 'Aún sin medallas'}"
            )
            await update.message.reply_text(texto_estado)
        else:
            await update.message.reply_text("Error al obtener tu estado.")

    elif texto == "✅ Completar":
        r = requests.post(f"{BACKEND_URL}/completar/{user_id}")
        if r.ok:
            await update.message.reply_text(r.json()["mensaje"])
        else:
            await update.message.reply_text("⚠️ Ya marcaste este día o hubo un error.")

    elif texto == "🔁 Repetir":
        r = requests.post(f"{BACKEND_URL}/repetir/{user_id}")
        if r.ok:
            await update.message.reply_text("🔁 Día repetido. Mañana recibirás el mismo contenido.")
        else:
            await update.message.reply_text("Error al repetir el día.")

    else:
        await update.message.reply_text("No entiendo ese comando, probá usar los botones.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_texto))

    app.run_polling()


if __name__ == "__main__":
    main()
