from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dictionary.dictionary import Dictionary
import constants as const

BOT_USERNAME = const.BOT_USERNAME
TOKEN = const.telegram_bot_token

class DictionaryBot:
    def __init__(self):
        self.app = Application.builder().token(TOKEN).build()
        self.add_handlers()

    def add_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("custom", self.custom_command))
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        self.app.add_error_handler(self.error_handler)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello, Ask anything here")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Help command")

    async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Custom command")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text

        if message_type == 'group':
            if BOT_USERNAME in text:
                text = text.replace(BOT_USERNAME, '')
                response = self.handle_response(text)  # Call synchronously
                await update.message.reply_text(response)
            else:
                print('Not for me')
        else:
            response = self.handle_response(text)  # Call synchronously
            await update.message.reply_text(response)
        print("Sent")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused error {context.error}")

    def handle_response(self, word: str):
        with Dictionary() as dictionary:  # Ensuring proper cleanup
            meaning = dictionary.find_word_meaning(word)
            return meaning if meaning else "No definition found."
    
    def run(self):
        print("Polling ...")
        self.app.run_polling(poll_interval=3)

