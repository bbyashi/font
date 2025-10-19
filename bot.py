import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


# ==========================
# ✍️ A4 Handwriting Generator (Auto Line Break + Black Ink)
# ==========================
def text_to_handwritten_page(text):
    # Create A4 page
    width, height = 1240, 1754  # A4
    img = Image.new("RGB", (width, height), color=(255, 255, 240))
    draw = ImageDraw.Draw(img)

    # Ruled lines
    top_margin = 180
    line_gap = 80
    for y in range(top_margin, height - 150, line_gap):
        draw.line((100, y, width - 100, y), fill=(200, 220, 255), width=2)

    # Font setup
    font_path = "fonts/Kalam-Regular.ttf"
    if not os.path.exists(font_path):
        font = ImageFont.truetype("arial.ttf", 46)
    else:
        font = ImageFont.truetype(font_path, 46)

    # Auto-wrap text
    wrapper = textwrap.TextWrapper(width=60)  # 60 chars per line (auto line break)
    lines = wrapper.wrap(text)

    # Start position
    x, y = 140, top_margin - 40

    for line in lines:
        draw.text((x, y), line, font=font, fill=(0, 0, 0))  # black ink
        y += line_gap

        # Safety: stop if page end reached
        if y > height - 200:
            break

    # Slight contrast for natural pen look
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)

    output_path = "handwritten_auto.jpg"
    img.save(output_path, quality=95)
    return output_path


# ==========================
# 🤖 Telegram Bot Handlers
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🖋️ Send me your text — I'll neatly write it on an A4 notebook page automatically (no \\n needed)."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("✍️ Writing your text neatly on an A4 page...")

    output = text_to_handwritten_page(user_text)
    await update.message.reply_photo(photo=open(output, "rb"))


# ==========================
# 🚀 Run the Bot
# ==========================
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("✅ A4 Handwriting Bot (Auto Line Break) Running...")
app.run_polling()
