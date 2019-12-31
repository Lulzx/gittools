#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import sys
import logging

from github import Github
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def fetch_url(url, query):
    params = urlencode({'q': query})
    final = url.format(params)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
    response = opener.open(final).read().decode('utf-8')
    dict_response = json.loads(response)
    return dict_response


def get_repo(query):
    base_url = 'https://api.github.com/search/repositories?{}&per_page=50'
    res = fetch_url(base_url, query)
    resp = []
    for item in res['items']:
        resp.append((item['html_url'], item['description']))
    return resp


def get_user(query):
    base_url = 'https://api.github.com/search/users?{}&per_page=50'
    res = fetch_url(base_url, query)
    respo = []
    for item in res['items']:
        respo.append((item['login'], item['html_url']))
    return respo


def search_callback(update, context):
    user_says = context.args # " ".join(context.args)
    query_type = user_says[0]
    query_term = user_says[1:]
    # make a tree structure for the list of repositories result
    update.message.reply_text("You said: " + user_says)


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    try:
        TOKEN = sys.argv[1]
    except IndexError:
        TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search", search_callback))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()