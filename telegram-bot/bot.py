from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Servidor dummy para Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"

# Ejemplo: función para obtener día actual de usuario (hardcode por ahora)
def get_dia_actual(user_id):
    # Aquí se debe leer la base de datos, por ahora devolvemos 5
    return 5

def start(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name or "Jefe"
    dia_actual = get_dia_actual(update.effective_user.id)

    welcome_text = f"¡Hola, {user_first_name}! Bienvenido al Protocolo R2. ¿Qué querés hacer hoy?"

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
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data
    responses = {
        'protocolo': "El Protocolo R2 es un programa diseñado para...",
        'receta_hoy': "Aquí está tu receta para hoy (Día actual).",
        'recetario': "Lista completa del recetario...",
        'agenda': "Tu agenda personal está vacía por ahora.",
        'lista_compras': "Aquí va tu lista de compras.",
        'tips': "Consejos útiles para tu progreso.",
        'logros': "Tus logros aparecerán aquí.",
        'recomendar': "Comparte este programa con tus amigos.",
        'ajustes': "Opciones de configuración.",
    }

    response_text = responses.get(data, "Opción no reconocida.")
    query.edit_message_text(response_text)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
