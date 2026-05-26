import os
import asyncio
import threading
import requests

from flask import Flask

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# =========================================
# CONFIG
# =========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://normaluser2.vercel.app/api/pinterest?url="

# =========================================
# FLASK WEB SERVER
# =========================================

web = Flask(__name__)


@web.route("/")
def home():

    return {
        "status": "online",
        "bot": "Pinterest Downloader",
        "developer": "@normaluser2",
        "made_by": "Jaxson"
    }


# =========================================
# START MESSAGE
# =========================================

START_TEXT = """
✨ *Pinterest Downloader*

Download Pinterest videos instantly in the highest available quality.

━━━━━━━━━━━━━━━━━━━

⚡ Ultra Fast Processing
🎬 High Quality Media
📥 Instant Delivery
🔗 Secure Downloads

━━━━━━━━━━━━━━━━━━━

📌 Send any Pinterest link to begin.

Example:
`https://pin.it/xxxxxxx`

━━━━━━━━━━━━━━━━━━━

⚠️ Videos are automatically removed after *10 minutes*.

Please save your media immediately after downloading.

━━━━━━━━━━━━━━━━━━━

👨‍💻 Developer: @normaluser2
❤️ Made by *Jaxson*
"""


# =========================================
# BUTTONS
# =========================================

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


# =========================================
# /START
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        START_TEXT,
        parse_mode="Markdown",
        reply_markup=premium_buttons(),
        disable_web_page_preview=True
    )


# =========================================
# HANDLE MESSAGE
# =========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # CHECK LINK
    if "pin.it" not in text and "pinterest.com" not in text:

        await update.message.reply_text(
            """
❌ *Invalid Link*

Please send a valid Pinterest URL.
            """,
            parse_mode="Markdown"
        )

        return

    try:

        # LOADING MESSAGE
        loading = await update.message.reply_text(
            """
✨ *Preparing Your Download*

━━━━━━━━━━━━━━━━━━━

🔍 Analyzing Pinterest media
⚡ Fetching highest quality
📦 Preparing secure delivery

━━━━━━━━━━━━━━━━━━━

Please wait...
            """,
            parse_mode="Markdown"
        )

        # API REQUEST
        r = requests.get(
            API + text,
            timeout=30
        ).json()

        # FAILED
        if not r.get("success"):

            await loading.edit_text(
                """
❌ *Download Failed*

Unable to process this Pinterest link.
                """,
                parse_mode="Markdown"
            )

            return

        # VIDEO
        video = r.get("best_video")

        # NO VIDEO
        if not video:

            await loading.edit_text(
                """
❌ *No Video Found*

This Pinterest post may not contain downloadable video media.
                """,
                parse_mode="Markdown"
            )

            return

        # SEND VIDEO
        await update.message.reply_video(
            video=video,
            caption="""
✨ *Download Complete*

━━━━━━━━━━━━━━━━━━━

🎬 Highest Quality Video Delivered
⚡ Processed Successfully

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

        # DELETE LOADING
        await loading.delete()

    except Exception as e:

        await update.message.reply_text(
            f"""
❌ *Unexpected Error*

`{str(e)}`
            """,
            parse_mode="Markdown"
        )


# =========================================
# TELEGRAM BOT
# =========================================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)


# =========================================
# RUN BOT
# =========================================

def run_bot():

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    app.run_polling(
        drop_pending_updates=True,
        close_loop=False,
        stop_signals=None
    )


# START BOT THREAD
threading.Thread(
    target=run_bot,
    daemon=True
).start()


# =========================================
# START WEB SERVER
# =========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    web.run(
        host="0.0.0.0",
        port=port
        )
