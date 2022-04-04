# -*- coding: utf-8 -*-

from pyrogram import emoji
from config import BOT_ID

RULES_URL = "https://telegra.ph/Pravila-chata-russkoj-Vikipedii-10-21"
MESSAGE = """
{} Добро пожаловать в чат русской Википедии.
Здесь действуют Универсальный кодекс поведения сообщества Викимедиа. [Полные правила чата]({}).
Для участия у вас должна быть учётная запись в Википедии.
[Авторизуйтесь через бота](tg://user?id={}), чтобы отправлять сообщения.
"""


async def welcome(client, message):
    text = MESSAGE.format(emoji.WAVING_HAND, RULES_URL, BOT_ID)
    await message.reply_text(text, disable_web_page_preview=True)
