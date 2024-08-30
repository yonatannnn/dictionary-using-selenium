from dictionary.dictionary import Dictionary
from telegram_bot.bot import DictionaryBot

def main():
    print("Starting ...")
    dictionary_bot = DictionaryBot()  # Initialize the Telegram bot
    dictionary_bot.run()

if __name__ == "__main__":
    main()
