from telegram import Update, InputSticker, StickerSet
from telegram.ext import Application, CommandHandler, ContextTypes

import asyncio

TOKEN = "6542403472:AAHAK-htx8g7WGNQw3zvmKwboPnewB9mRtQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, For recieving the sticker, press the /sticker link")

async def send_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker_id = ""
    await update.message.reply_sticker(sticker= sticker_id)

# For searching the sticker
async def search_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = "".join(context.args) if context.args else "hello"
    if stickers.stickers:
        await update.message.reply_sticker(sticker= stickers.stickers[0].file_id)

# get sticker file id
async def get_sticker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.sticker:
        sticker_id = update.message.sticker.file_id
        await update.message.reply_text(f"The ID of the sticker is : {sticker_id}")

# uploading new sticker
async def uplaod_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''.webp is the telegram sticker format'''
    with open("sticker.webp", "rb") as sticker_file:
        await update.message.reply_sticker(sticker= sticker_file)


def main():
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_sticker", send_sticker))
    application.add_handler(CommandHandler("search_sticker", search_sticker))
    application.add_handler(CommandHandler("get_sticker_id", get_sticker_id))
    application.add_handler(CommandHandler("upload_sticker", upload_sticker))

    application.run_polling()



if __name__ == "__main__":
    main()

