from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ChatMemberHandler
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy HTTP server para mantener vivo Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

TOKEN = "TU_TOKEN_AQUI"

def send_menu(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name or "Querid@ Amig@"
    dia_actual = 5

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
        update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

def start(update: Update, context: CallbackContext):
    send_menu(update, context)

def chat_member_update(update: Update, context: CallbackContext):
    chat_member = update.chat_member
    if chat_member.new_chat_member.status == 'member':
        send_menu(update, context)

def main():
    while True:
        try:
            updater = Updater(TOKEN)
            dp = updater.dispatcher

            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))
            dp.add_handler(CallbackQueryHandler(callback_handler))  # Define callback_handler si tienes

            updater.start_polling()
            logger.info("Bot iniciado correctamente.")
            updater.idle()
        except Exception as e:
            logger.error(f"Error en el bot: {e}")
            time.sleep(5)  # Espera 5 segundos antes de intentar reconectar

if __name__ == '__main__':
    main()
