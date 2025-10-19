from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

# ========== CONFIG ==========
BOT_TOKEN = "8388314171:AAFXrRKZU0d7XMRP5sRNi89ixXXzYGo0_Ws"
FONT_PATH = "QEAntonyLark.ttf"
FONT_SIZE = 72
MARGIN_LEFT = 250
MARGIN_TOP = 300
LINE_SPACING = 120
CHAR_LIMIT = 40

# ========== FUNCTION TO GENERATE HANDWRITTEN IMAGE ==========
def generate_handwritten_image(text):
    page_width, page_height = 2480, 3508  # A4 size at 300 DPI
    page = Image.new("RGB", (page_width, page_height), "white")
    draw = ImageDraw.Draw(page)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # ----- Draw horizontal blue lines (like notebook paper) -----
    line_color = (180, 210, 255)  # soft blue
    y = MARGIN_TOP - 20
    while y < page_height - 200:
        draw.line((100, y, page_width - 100, y), fill=line_color, width=3)
        y += LINE_SPACING

    # ----- Draw left margin (red line) -----
    margin_x = MARGIN_LEFT - 80
    draw.line((margin_x, MARGIN_TOP - 100, margin_x, page_height - 200), fill=(255, 80, 80), width=5)

    # ----- Write text -----
    paragraphs = text.split("\n")
    x, y = MARGIN_LEFT, MARGIN_TOP

    for para in paragraphs:
        if para.strip() == "":
            y += LINE_SPACING
            continue

        wrapped = textwrap.wrap(para, width=CHAR_LIMIT)
        for line in wrapped:
            # random pen-like blue tone
            color = (random.randint(20, 40), random.randint(20, 40), random.randint(160, 210))
            draw.text((x, y), line, font=font, fill=color)
            y += LINE_SPACING
        y += LINE_SPACING // 2

    output_path = "handwritten_output.jpg"
    page.save(output_path, "JPEG")
    return output_path

# ========== BOT HANDLER ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("🖋 Writing your text with blue ink on lined paper...")
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
