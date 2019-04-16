#!/usr/bin/env python3
import telegram
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
        update.message.reply_text('This isn\'t good...')


def add_schedule(bot, update):
    """
    Add Schedule
    """
    try:
        if not sqh.chat_has_schedule(update.message.chat_id):
            if update.message.text.split('/add_schedule')[1] != '':
                sched = sqh.add_schedule(
                    chat_id=update.message.chat_id,
                    schedule_title=update.message.text.split(
                        '/add_schedule')[1].strip()
                )
                if sched:
                    bot.sendMessage(
                        update.message.chat_id,
                        text=('A schedule has been created!')
                    )
                    print("[+] Added schedule!")
                else:
                    bot.sendMessage(
                        update.message.chat_id,
                        text=('Unkknown error try again :c')
                    )
                    print("[!] Error adding schedule")
            else:
                bot.sendMessage(
                    update.message.chat_id,
                    text=(
                        'Please provide a title by typing additional text' +
                        ' after \'/add_schedule\''
                    )
                )

        else:
            bot.sendMessage(
                update.message.chat_id,
                text=('Currently only 1 schedule per chat is supported :3')
            )

    except:
        update.message.reply_text('This isn\'t good...')


def schedule(bot, update):
    sched = sqh.get_schedule(update.message.chat_id)
    if sched:
        msg = '<b>{0}</b>\n<strong>Tasks:</strong>'.format(sched.title)
        if sched.tasks:
            for i in range(len(sched.tasks)):
                task = sched.tasks[i]
                msg += '\n<b>{0}:</b> {1}'.format(i, task.title)
                if task.datetime:
                    msg += '\n<b>Date/TIme: </b> {0}'.format(task.datetime)
                if task.location:
                    msg += '\n<b>Location: </b> {0}'.format(task.location)
                if task.description:
                    msg += '\n<b>Description: </b> {0}'.format(
                        task.description)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.HTML
        )
    else:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Sorry there is no schedule for this chat.'
        )


def add_task(bot, update):
    """
    Add task
    """
    try:
        if sqh.chat_has_schedule(update.message.chat_id):
            if update.message.text.split('/add_task')[1] != '':
                sched = sqh.add_task(
                    chat_id=update.message.chat_id,
                    task_title=update.message.text.split(
                        '/add_task')[1].strip()
                )
                if sched:
                    bot.sendMessage(
                        update.message.chat_id,
                        text=('A task has been created!')
                    )
                    print("[+] Added task!")
                else:
                    bot.sendMessage(
                        update.message.chat_id,
                        text=('Unkknown error try again :c')
                    )
                    print("[!] Error adding task")
            else:
                bot.sendMessage(
                    update.message.chat_id,
                    text=(
                        'Please provide a title by typing additional text' +
                        ' after \'/add_task\''
                    )
                )

        else:
            bot.sendMessage(
                update.message.chat_id,
                text=('Currently no schedule exists')
            )

    except:
        update.message.reply_text('This isn\'t good...')


def help(bot, update):
    """
    Send a message when the command /help is issued.
    """
    bot.sendMessage(
        update.message.chat_id,
        text=(
            'Commands:\n' +
            '/start | activate bot\n' +
            '/help | help menu\n' +
            '/addschedule | add schedule\n' +
            '/schedule | display schedule'
        )
    )


def main():
    """Start the bot."""
    #updater = Updater(config.BOT_TOKEN)
    updater = Updater(config.BOT_TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(
        CommandHandler(
            "add_schedule",
            add_schedule
        )
    )
    dp.add_handler(
        CommandHandler(
            "schedule",
            schedule
        )
    )

    # Start the Bot
    print('[+] Bot is active!')
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
