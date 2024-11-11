from dictionary.dictionary import Dictionary
from telegram_bot.bot import DictionaryBot

def main():
    print("Starting ...")
    dictionary_bot = DictionaryBot()
    dictionary_bot.run()

if __name__ == "__main__":
    main()
