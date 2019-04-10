#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler

from config import config
from sqlhelper import sqlhelper

sqh = sqlhelper.SQLHelper(config.DB)


def start(bot, update):
    """
    Send a message when the command /start is issued.
    """
    update.message.reply_text('Good day!')
    try:
        if not sqh.is_duplicate_chat(update.message.chat_id):
            sqh.add_chat(update.message.chat_id)
            bot.sendMessage(
                update.message.chat_id,
                text=(
                    'This Chat has been added to my database.' +
                    ' I can now take requests!'
                )
            )
            print("[+] Added chat!")
        else:
            bot.sendMessage(
                update.message.chat_id,
                text=(
                    'Thanks for the enthusiasm! ' +
                    'But this Chat is already registered.'
                )
            )

    except:
        update.message.reply_text('This isn\'t good..')


def help(bot, update):
    """
    Send a message when the command /help is issued.
    """
    bot.sendMessage(
        update.message.chat_id,
        text=(
            'Commands:\n' +
            '/start | activate bot\n' +
            '/help | help menu'
        )
    )


def main():
    """Start the bot."""
    updater = Updater(config.BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Start the Bot
    print('[+] Bot is active!')
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
