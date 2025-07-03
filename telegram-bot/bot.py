from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ChatMemberHandler
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Servidor dummy para que Render detecte puerto abierto
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"  # Reemplaza si cambia

def send_menu(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name or "Querid@ Amig@"
    dia_actual = 5  # Puedes sacar de DB luego

    welcome_text = (
        f"¡Hola, {user_first_name}! Bienvenid@ al Protocolo R2.\n\n"
        "Este es un camino de renovación y energía.\n"
        "Cada día es un paso hacia una versión más saludable y poderosa de ti mism@.\n"
        "¡Vamos con todo, que la transformación comienza ahora!\n\n"
        "¿Qué querés hacer hoy?"
    )

    keyboard = [
        [InlineKeyboardButton("📖 Qué es el Protocolo R2", callback_data='protocolo')],
        [InlineKeyboardButton(f"🥗 Mi receta de hoy (📆 Día {dia_actual})", callback_data='receta_hoy')],
        [InlineKeyboardButton("📚 Recetario completo", callback_data='recetario')],
        [InlineKeyboardButton("✍️ Mi agenda personal", callback_data='agenda')],
        [InlineKeyboardButton("🛍️ Lista de compras", callback_data='lista_compras')],
        [InlineKeyboardButton("💡 Tips y ayuda", callback_data='tips')],
        [InlineKeyboardButton("🎯 Mis logros", callback_data='logros')],
        [InlineKeyboardButton("📢 Recomendar programa", callback_data='recomendar')],
        [InlineKeyboardButton("⚙️ Ajustes", callback_data='ajustes')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
