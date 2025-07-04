from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# === CONFIGURACIÓN DEL BOT ===
TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"
WEBHOOK_PATH = f"/webhook/{TOKEN}"

bot = Bot(token=TOKEN)
app = FastAPI()
application = Application.builder().token(TOKEN).build()

# === COMANDOS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    mensaje = (
        f"🌿 *Querido Amig@* {nombre},\n\n"
        "Bienvenid@ al Protocolo R2.\n"
        "Este es un viaje de transformación profunda, energía y salud.\n\n"
        "🧠 *Recuerda*: tu cuerpo es sabio, tu decisión poderosa.\n"
        "Estoy aquí para acompañarte día a día.\n\n"
        "📋 Usa el menú para comenzar."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))

# === RUTAS ===
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"ok": True}

@app.get("/")
def home():
    return {"status": "bot running via webhook"}
