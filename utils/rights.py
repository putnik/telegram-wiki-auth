# -*- coding: utf-8 -*-

from config import CHAT_ID


def set_rights(client, tg_id: int):
    client.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=tg_id,
        can_edit_messages=True,
        can_invite_users=True,
    )


def remove_rights(client, tg_id: int):
    client.promote_chat_member(
        chat_id=CHAT_ID,
        user_id=tg_id,
        can_edit_messages=False,
        can_invite_users=False,
    )
