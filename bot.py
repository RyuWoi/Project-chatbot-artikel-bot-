import os
import requests
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackContext

# Muat variabel dari file .env
load_dotenv()
api_token = os.getenv("TELEGRAM_API_TOKEN")

async def get_wikipedia_summary(search_term: str) -> str:
    url = "https://id.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": search_term
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_data in pages.items():
        if page_id != "-1":
            return page_data.get("extract", "Ringkasan tidak ditemukan.")
    return "Artikel tidak ditemukan di Wikipedia."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya adalah Wikipedia Chatbot. Ketik 'Wikipedia <kata kunci>' untuk mencari ringkasan artikel.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if user_input.lower().startswith("wikipedia "):
        search_term = user_input[10:]
        summary = await get_wikipedia_summary(search_term)
        await update.message.reply_text(summary)
    else:
        await update.message.reply_text("Maaf, saya tidak mengerti. Coba ketik 'Wikipedia <kata kunci>' untuk mencari ringkasan artikel.")

# Daftar pantun
pantun_list = [
    "Jalan-jalan ke pasar baru,\nPulang-pulang beli sepatu.\nWahai kamu yang tampan dan ayu,\nTetaplah semangat tanpa ragu.",
    "Ada kapal di tengah laut,\nBerlayar jauh tak tentu arah.\nMeski rintangan selalu mengahut,\nTetap berjuang jangan menyerah.",
    "Ke kebun memetik jambu,\nJambu manis untuk diramu.\nHai teman, selamat berjumpa,\nSemoga hari penuh ceria selalu.",
    "Burung perkutut di atas dahan,\nBerkicau merdu di pagi buta.\nSelalu semangat dalam perjuangan,\nSukses datang pada yang berusaha."
]

# Fungsi untuk menangani perintah /pantun
async def send_pantun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from random import choice
    pantun = choice(pantun_list)  # Pilih pantun secara acak
    await update.message.reply_text(pantun)

def main():
    # Periksa apakah API token ada
    if not api_token:
        print("Error: Token API Telegram tidak ditemukan.")
        return

    # Inisialisasi aplikasi bot
    app = Application.builder().token(api_token).build()

    # Handler untuk memulai bot
    app.add_handler(CommandHandler("start", start))
    
    # Handler untuk pesan teks
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    
     # Tambahkan handler untuk perintah /pantun
    app.add_handler(CommandHandler('pantun', send_pantun))

    # Jalankan bot
    app.run_polling()

if __name__ == "__main__":
    main()
