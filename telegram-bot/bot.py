from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ChatMemberHandler
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ================= Dummy server para Render ===================
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# ================= Bot de Telegram ============================
TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"  # No lo compartas públicamente

def send_menu(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name or "Querid@ Amig@"
    dia_actual = 5  # Podés cambiarlo luego dinámicamente

    welcome_text = (
        f"¡Hola, {user_first_name}! Bienvenid@ al *Protocolo R2*.\n\n"
        "✨ Este es un camino de renovación y energía.\n"
        "Cada día es un paso hacia una versión más saludable y poderosa de vos mism@.\n"
        "💪 ¡Vamos con todo, que la transformación comienza ahora!\n\n"
        "*¿Qué querés hacer hoy?*"
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
        update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    respuestas = {
        "protocolo": "El Protocolo R2 es un programa de desintoxicación integral...",
        "receta_hoy": "Tu receta de hoy: 🥒 Ensalada de pepino con limón y perejil.",
        "recetario": "Aquí va el recetario completo. Próximamente disponible.",
        "agenda": "Tu agenda personal aún no está configurada.",
        "lista_compras": "Lista de compras para esta semana: 🍅🥬🍋...",
        "tips": "Tip de hoy: Tomá mucha agua durante la fase de desintoxicación.",
        "logros": "Todavía no registraste logros. ¡Empecemos!",
        "recomendar": "Compartí este programa con tus amig@s 💌",
        "ajustes": "Ajustes: próximamente disponible."
    }

    respuesta = respuestas.get(query.data, "Opción no disponible.")
    query.edit_message_text(respuesta)

def greet_new_user(update: Update, context: CallbackContext):
    result = update.chat_member
    if result.new_chat_member.status == "member":
        send_menu(update, context)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", send_menu))
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    dispatcher.add_handler(ChatMemberHandler(greet_new_user, ChatMemberHandler.CHAT_MEMBER))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
