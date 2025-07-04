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

TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"  # Tu token

def send_menu(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name or "Querid@ Amig@"
    dia_actual = 5  # Aquí luego conectarás con DB para traer el día real

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

def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data
    # Respuestas de ejemplo para cada botón (luego los conectamos con lógica real)
    responses = {
        'protocolo': "El Protocolo R2 es un camino de desintoxicación y renovación para tu cuerpo y mente.",
        'receta_hoy': "Aquí está tu receta para hoy... (a implementar).",
        'recetario': "Accede al recetario completo en https://tusitio.com/recetario",
        'agenda': "Tu agenda personal está en desarrollo.",
        'lista_compras': "Tu lista de compras aparecerá pronto.",
        'tips': "Tip del día: Bebe mucha agua y mantente activo.",
        'logros': "¡Vas genial! Aquí están tus logros... (a implementar).",
        'recomendar': "Comparte este programa con tus amigos y familiares.",
        'ajustes': "Configura tus preferencias aquí (próximamente).",
    }

    text = responses.get(data, "Funcionalidad en desarrollo.")
    query.edit_message_text(text=text)

def welcome_new_member(update: Update, context: CallbackContext):
    # Cuando un usuario se une, enviamos el menú
    chat_member = update.chat_member
    if chat_member.new_chat_member.status == 'member':
        send_menu(update, context)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_button))
    dp.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
