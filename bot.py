# bot.py
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
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
    # יצירת האובייקט Updater
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # קבלת ה-Dispatcher למתן גישה לרגיסטרציה של ה-handlers
    dispatcher = updater.dispatcher

    # רישום הפונקציה start כ-handler לפקודת /start
    dispatcher.add_handler(CommandHandler("start", start))

    # רישום הפונקציה handle_message כ-handler להודעות טקסט
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # רישום הפונקציה error כ-handler לשגיאות
    dispatcher.add_error_handler(error)

    # הפעלת הבוט
    updater.start_polling()

    # שמירה על הפעולה של הבוט עד להפסקה
    updater.idle()

if __name__ == '__main__':
    main()
