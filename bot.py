import logging
import os

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from database import users, games
from jobs import check_if_game_has_changed
from scrapers import scraper, utilities

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'fALSEvaLuE')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

last_commands = {}


def start(update, context):
    """Message user on /start"""
    user_ = update.message.from_user
    # save user to db
    users.insert_one({
        "chat_id": user_['id'],
        "username": user_['first_name'],
        "last_command": "",
        "games": []
    })
    update.message.reply_text(f'Hello {user_["first_name"]}')


def check_games(update, context):
    chat_id = update.effective_chat.id
    user = users.find_one({'chat_id': chat_id})
    if user:
        user_last_command = user.get('last_command')
    else:
        return
    if user_last_command == "check_bet":
        ticker = update.message.text
        # save game id to users and games collections
        users.update_one({'chat_id': chat_id}, {"$addToSet": {"games": ticker}})
        if not games.find_one({'ticket': ticker}):
            games.insert_one({'ticket': ticker, 'users': [], 'finished': False})
        else:
            games.update_one({'ticket': ticker}, {"$addToSet": {'users': chat_id}})

        retrieved_games = scraper.get_games(ticker, chat_id)
        text = utilities.format_data(retrieved_games)
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='MarkdownV2'
        )
    # update.message.reply_text(update.message.text)


def get_user_game(update, context):
    if users.find_one({'chat_id': update.message.chat_id}):
        users.update_one({'chat_id': update.message.chat_id}, {
            "$set": {
                "last_command": 'check_bet'
            }
        })
        update.message.reply_text("Enter Sporty Code: ")
    else:
        update.message.reply_text("You need to press the start command to use me.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


updater = Updater(TOKEN, use_context=True)
job = updater.job_queue


def game_update_callback(context: telegram.ext.CallbackContext):
    check_if_game_has_changed()


job.run_repeating(game_update_callback, 30)


def main():
    dp = updater.dispatcher  # get dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('echo', check_games))
    dp.add_handler(CommandHandler('check_bet', get_user_game))

    dp.add_handler(MessageHandler(Filters.text, check_games))
    dp.add_error_handler(error)
    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://sporty-bet-bot.herokuapp.com' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
