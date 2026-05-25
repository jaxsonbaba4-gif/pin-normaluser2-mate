import os
import threading
import requests

from flask import Flask

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://normaluser2.vercel.app/api/pinterest?url="

app = Flask(__name__)


# UPTIME ROUTE
@app.route("/")
def home():
    return {
        "status": "online",
        "bot": "Pinterest Downloader",
        "developer": "@normaluser2"
    }


START_TEXT = """
✨ *Pinterest Downloader*

Download Pinterest videos instantly in the highest available quality.

━━━━━━━━━━━━━━━━━━━

⚡ Ultra Fast Processing  
🎬 High Quality Media  
📥 Instant Delivery  
🔗 Clean & Secure Downloads  

━━━━━━━━━━━━━━━━━━━

📌 Send any Pinterest link to begin.

Example:
`https://pin.it/xxxxxxx`

━━━━━━━━━━━━━━━━━━━

⚠️ Downloaded videos are automatically removed after *10 minutes*.

Please save your media immediately after downloading.

━━━━━━━━━━━━━━━━━━━

❤️ Crafted with precision by *Jaxson*
"""


def premium_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Buy API",
                url="https://t.me/normaluser2"
            )
        ],
        [
            InlineKeyboardButton(
                "👨‍💻 Developer",
                url="https://t.me/normaluser2"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        START_TEXT,
        parse_mode="Markdown",
        reply_markup=premium_buttons(),
        disable_web_page_preview=True
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if "pin.it" not in text and "pinterest.com" not in text:

        await update.message.reply_text(
            "❌ Please send a valid Pinterest link.",
            parse_mode="Markdown"
        )

        return

    try:

        loading = await update.message.reply_text(
            """
✨ *Preparing Your Download*

━━━━━━━━━━━━━━━━━━━

🔍 Analyzing Pinterest media  
⚡ Fetching highest quality  
📦 Finalizing secure delivery  

━━━━━━━━━━━━━━━━━━━

Please wait...
            """,
            parse_mode="Markdown"
        )

        r = requests.get(API + text).json()

        if not r.get("success"):

            await loading.edit_text(
                "❌ Failed to fetch media."
            )

            return

        video = r.get("best_video")

        if not video:

            await loading.edit_text(
                "❌ No downloadable video found."
            )

            return

        await update.message.reply_video(
            video=video,
            caption="""
✨ *Download Complete*

━━━━━━━━━━━━━━━━━━━

🎬 Highest Quality Video Ready  
⚡ Delivered Successfully  

━━━━━━━━━━━━━━━━━━━

⚠️ This video will be automatically removed after *10 minutes*.

Please save your media before it expires.

━━━━━━━━━━━━━━━━━━━

👨‍💻 Developer: @normaluser2  
❤️ Made by *Jaxson*
            """,
            parse_mode="Markdown",
            supports_streaming=True,
            reply_markup=premium_buttons()
        )

        await loading.delete()

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n`{str(e)}`",
            parse_mode="Markdown"
        )


telegram_app = Application.builder().token(BOT_TOKEN).build()

telegram_app.add_handler(
    CommandHandler("start", start)
)

telegram_app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)


def run_bot():
    telegram_app.run_polling()


# START BOT THREAD
threading.Thread(target=run_bot).start()
