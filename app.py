import os
import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Token del bot (heroku leerá la variable de entorno)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7635694098:AAH4nhsvOszEFsIF0-Ali-NgVWD7bHKZF6U")

# Configuración de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Mensajes Otaku
WELCOME_MSG = "✨ いらっしゃいませ! Bienvenido/a al grupo, nakama 🍥"
SPAM_MSG = "⚔️ ¡Alto ahí! Eso parece spam. En este dojo no está permitido ❌"
BLOCK_MSG = "🚫 Usuario baneado por comportamiento sospechoso 👹"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kon'nichiwa ☀️! Soy ModerationSat_bot estilo Otaku. Usa /help para ver mis poderes ✨")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Comandos de Moderación:\n"
        "/ban - Expulsar usuario 🚫 (responde al mensaje)\n"
        "/pin - Anclar mensaje 📌 (responde al mensaje)\n"
        "/mute - Silenciar 🔇 (responde al mensaje)\n"
        "/unmute - Activar 🔊 (responde al mensaje)"
    )

# /ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Responde al mensaje del usuario que quieras banear ❌")
        return
    user_id = update.message.reply_to_message.from_user.id
    await update.effective_chat.ban_member(user_id)
    await update.message.reply_text(BLOCK_MSG)

# /pin
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.message.reply_to_message.pin()
        await update.message.reply_text("📌 Mensaje anclado con poder ninja ✨")

# /mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Responde al mensaje del usuario que quieras silenciar 🔇")
        return
    user_id = update.message.reply_to_message.from_user.id
    await update.effective_chat.restrict_member(user_id, ChatPermissions(can_send_messages=False))
    await update.message.reply_text("🔇 Usuario silenciado. Que aprenda disciplina 🥋")

# /unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Responde al mensaje del usuario que quieras reactivar 🔊")
        return
    user_id = update.message.reply_to_message.from_user.id
    await update.effective_chat.restrict_member(
        user_id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True
        )
    )
    await update.message.reply_text("🔊 Usuario reactivado, regresa a la batalla ⚔️")

# Anti-spam básico
async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text and ("http" in text or "www" in text):
        await update.message.delete()
        await update.message.reply_text(SPAM_MSG)

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("pin", pin))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))

    # Anti-spam
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))

    app.run_polling()

if __name__ == "__main__":
    main()
