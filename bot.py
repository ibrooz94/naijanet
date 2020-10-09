import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telenaijanet import get_search_result, final_pass, sub_pass
from credentials import TOKEN, URL
PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat.first_name
    update.message.reply_text('Hello %s, I\'m Naijanetbot😎\nI help download the latest movies and videos from netnaija without ads✨.\nℹ For more info and tips /help' %chat_id)
    update.message.reply_text('Enter movie name::  ')

def download(update, context):
    """Echo the user message."""
    search_result = get_search_result(update.message.text)
    search_result = search_result[:3]

    if search_result:
        end_result = []
        for i in search_result:
            try:
                end_result.append({
                    "name" :i["name"],
                    "url" : final_pass(i["url"]),
                    "sub": sub_pass(i["url"])
                    })
            except IndexError:
                continue
    else:
        update.message.reply_text("No download availble (╯‵□′)╯︵┻━┻")

    if end_result:
        for i in end_result:
            name= i["name"]
            url = i["url"]
            sub = i["sub"]
            if sub:
                keyboard = [
                    [InlineKeyboardButton("Download 🔥", url=url)],
                    [InlineKeyboardButton("Subtitle 📝", url=sub)]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("Download 🔥", url=url)]
                ]
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(name, reply_markup=reply_markup)
    else:
        update.message.reply_text("No download availble ಠ﹏ಠ")

def button(update, context):
    query = update.callback_query
    query.answer()


def help_command(update, context):
    update.message.reply_text("For series, be specific Enter name, season and episode number (e.g The Boys S1E3)")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook(URL + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
