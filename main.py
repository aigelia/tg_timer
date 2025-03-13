import os
import time

from decouple import config
import ptbot
from pytimeparse import parse


TG_TOKEN = config('TELEGRAM_TOKEN')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def create_timer(chat_id, message, bot):
    message_id = bot.send_message(chat_id, 'Запускаю таймер...')
    time.sleep(1)
    total = parse(message)
    bot.create_countdown(
        parse(message),
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total=total,
        bot=bot
    )


def notify_progress(secs_left, chat_id, message_id, total, bot):
    bot.update_message(
        chat_id,
        message_id,
        "Осталось {} секунд \n{}".format(secs_left, render_progressbar(total, total - secs_left))
    )
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло!")


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(create_timer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
