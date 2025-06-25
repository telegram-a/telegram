#pylint:disable=C0114
import logging
import os
from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.errors import BadRequest
# import asyncio
# from pyrogram.errors import FloodWait
# from pyrogram.handlers import MessageHandler
# os.environ['TZ'] = 'Asia/Kolkata'



logging.basicConfig(level=logging.INFO)



bot = Client(
    'bot',
    api_id= API_ID, #get it from https://my.telegram.org/auth
    api_hash="", #get it from https://my.telegram.org/auth
    bot_token="7952311570:AAHmtHkN-kA5Gy1pF4BMk8NZdhAZpB5mnCg", #get it from @Botfather
    plugins=dict(root="plugins"),
    parse_mode="html")


try:
    bot.run()
except Exception as e:
    print(e)
    