# bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import TELEGRAM_BOT_TOKEN
from gpt_handler import gpt_response, detect_language

# הפעלת logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# פונקציה להתחלת הבוט
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('שלום סלבה')

# פונקציה לטיפול בהודעות ולהפעלת GPT
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    language = detect_language(user_input)
    response = gpt_response(user_input, language)
    update.message.reply_text(response)

# פונקציה לטיפול בשגיאות
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # יצירת האובייקט Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # רישום הפונקציה start כ-handler לפקודת /start
    application.add_handler(CommandHandler("start", start))

    # רישום הפונקציה handle_message כ-handler להודעות טקסט
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # רישום הפונקציה error כ-handler לשגיאות
    application.add_error_handler(error)

    # הפעלת הבוט
    application.run_polling()

if __name__ == '__main__':
    main()
