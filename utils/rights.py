# -*- coding: utf-8 -*-

from config import CHAT_ID
from pyrogram.types import ChatPermissions


def set_rights(client, tg_id: int):
    client.restrict_chat_member(CHAT_ID, tg_id, ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
    ))


def remove_rights(client, tg_id: int):
    client.restrict_chat_member(CHAT_ID, tg_id, ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_add_web_page_previews=False,
        can_invite_users=False,
    ))
