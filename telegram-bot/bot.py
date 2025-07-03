from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Servidor dummy para que Render detecte puerto abierto ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

# Iniciar el servidor dummy en hilo separado
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- Código original del bot ---
TOKEN = "8008692642:AAFkxddcVfOlp8YHKqpcgiCkEVplkup5qEs"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola, Jefe! Bot listo para usar.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Inicia el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
