from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# ========== CONFIG ==========
BOT_TOKEN = "8388314171:AAFXrRKZU0d7XMRP5sRNi89ixXXzYGo0_Ws"
FONT_PATH = "QEAntonyLark.ttf"
FONT_SIZE = 72
MARGIN_LEFT = 250
MARGIN_TOP = 300
LINE_SPACING = 120

# ========== FUNCTION TO GENERATE HANDWRITTEN IMAGE ==========
def generate_handwritten_image(text):
    # Create blank white A4 page
    page_width, page_height = 2480, 3508
    page = Image.new("RGB", (page_width, page_height), "white")
    draw = ImageDraw.Draw(page)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Split text into lines respecting user-entered newlines
    lines = text.splitlines()

    x, y = MARGIN_LEFT, MARGIN_TOP
    for line in lines:
        # Wrap each logical line separately
        wrapped_lines = textwrap.wrap(line, width=40)
        if not wrapped_lines:
            # Empty line (user pressed Enter twice)
            y += LINE_SPACING
        for subline in wrapped_lines:
            draw.text((x, y), subline, font=font, fill=(0, 0, 0))
            y += LINE_SPACING

    output_path = "handwritten_output.jpg"
    page.save(output_path, "JPEG")
    return output_path

# ========== BOT HANDLER ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("🖋 Writing your text neatly on an A4 page...")
    image_path = generate_handwritten_image(text)
    await update.message.reply_photo(photo=open(image_path, "rb"))

# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
