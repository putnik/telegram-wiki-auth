# -*- coding: utf-8 -*-

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from commands.log import log
from commands.auth import auth_start, auth_link, auth_forget, auth_process
from commands.welcome import welcome
from config import API_ID, API_HASH, CHAT_ID

from utils.logs import init_logs_table
from utils.tokens import init_states_table
from utils.users import init_users_table


init_logs_table()
init_states_table()
init_users_table()

app = Client("auth", API_ID, API_HASH)

# auth
app.add_handler(MessageHandler(auth_link, filters.private & ~filters.me & filters.command('auth')))
app.add_handler(MessageHandler(auth_forget, filters.private & ~filters.me & filters.command('forget')))
app.add_handler(MessageHandler(auth_start, filters.private & ~filters.me & filters.command('start')))
app.add_handler(MessageHandler(auth_process, filters.private & ~filters.me & filters.command('process')))

app.add_handler(MessageHandler(welcome, filters.chat(CHAT_ID) & filters.new_chat_members))
app.add_handler(MessageHandler(log))
app.run()
