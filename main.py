#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from github import Github
from uuid import uuid4
import emojis
import logging
import os
import sys
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode
from telegram import InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

logging.basicConfig(format='%(asctime)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

access_token = os.environ.get("access_token")
g = Github(access_token)


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def fetch_url(query_term, query_type):
    if query_type in ["u", "user"]:
        result = get_user(query_term)
    elif query_type in ["r", "repo"]:
        result = get_repo(query_term)
    else:
        result = "NIL"
    return result


def get_repo(query):
    repo = g.get_repo(query)
    name = repo.name
    repo_url = repo.html_url
    clone_url = repo.clone_url
    # description = repo.description
    stars = repo.stargazers_count
    language = repo.language
    owner_name = repo.owner.name
    owner_url = repo.owner.html_url
    response = f"""🗄 [{name}]({repo_url}) by [{owner_name}]({owner_url})"""
    response += f""" in #{language}\n⭐️ {stars} Stars\n📥 [Clone]({clone_url})"""
    return response


def get_user(query):
    user = g.get_user(query)
    name = "👥 " + user.name
    location = "📌 " + user.location
    bio = "🎭 " + user.bio
    # avatar = user.avatar_url
    response = "{}\n{}\n{}".format(name, location, bio)
    response += "\n🔗 https://github.com/{}".format(query)
    return response


def search_callback(update, context):
    user_says = context.args
    if len(user_says):
        chat_id = update.message.chat.id
        query_type = str(user_says[0])
        query_term = str(user_says[1:][0])
        result = fetch_url(query_term, query_type)
        link = result.split("[Clone](")[-1][:-1]
        data = result.split(".")[1].split("/")
        base = "https://github.com/"
        username = data[1]
        # repo_name = data[2]
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("👤 profile", url=str(base+username)), InlineKeyboardButton("🗄 repository", url=link)]])
        context.bot.send_message(chat_id=chat_id, text="{}".format(result), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    else:
        return


def download(update, context):
    user_says = context.args
    chat_id = update.message.chat.id
    # query_type = str(user_says[0])
    query_term = str(user_says[0])
    url = f"https://github.com/{query_term}/archive/master.zip"

    caption = f"✅ download successful for repository: {query_term}"
    context.bot.send_document(chat_id=chat_id, document=url, caption=caption)
    # except:
    #   context.bot.send_message(chat_id=chat_id, text="repository not found!")


def emoji_callback(update, context):
    chat_id = update.message.chat.id
    emojiset = g.get_emojis()
    for x in emojiset:
        x = f":{x}:"
        context.bot.send_message(chat_id=chat_id, text=emojis.encode(x))
        time.sleep(0.1)


def inlinequery(update, context):
    try:
        query = update.inline_query.query.split(" ")
        query_type = query[0]
        query_term = query[1]
    except:
        return
    result = fetch_url(query_term, query_type)
    title = "Result"
    if result is "NIL":
        title = "No results found."
        result = "No results found."
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=title,
            input_message_content=InputTextMessageContent(
                "{}".format(result),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results, cache_time=3)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    try:
        TOKEN = sys.argv[1]
    except IndexError:
        TOKEN = os.environ.get("telegram_token")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search", search_callback))
    dp.add_handler(CommandHandler("emoji", emoji_callback))
    dp.add_handler(CommandHandler("download", download))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
