# -*- coding: utf-8 -*-

from authlib.integrations.requests_client import OAuth2Session
from config import CHAT_ID, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_AUTH_ENDPOINT
from utils.logs import log
from utils.rights import set_rights, remove_rights
from utils.tokens import create_state
from utils.users import get_all_ids, get_username, delete_user

tg_ids = None


def is_authorized(user):
    global tg_ids
    if tg_ids is None:
        tg_ids = get_all_ids()
    return user.id in tg_ids or user.is_bot


async def auth_start(client, message):
    log(message, 'start')

    username = get_username(message.from_user.id)
    if username is None:
        await auth_link(client, message)
        return

    await set_rights(client, message.from_user.id)
    answer = '''
Всё отлично! Вы авторизованы как [%s](https://ru.wikipedia.org/wiki/User:%s).
Теперь вы можете отправлять сообщения в чате.
    ''' % (username, username)
    await message.reply(answer, disable_web_page_preview=True)


async def auth_link(client, message):
    auth_client = OAuth2Session(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET)
    url, state = auth_client.create_authorization_url(OAUTH_AUTH_ENDPOINT, response_type='code')
    log(message, 'link', url)

    create_state(state, message.from_user.id, message.from_user.username)
    answer = "Для авторизации перейдите по [ссылке](%s)." % url
    await message.reply(answer, disable_web_page_preview=True)


async def auth_forget(client, message):
    log(message, 'forget')
    delete_user(message.from_user.id)
    await remove_rights(client, message.from_user.id)

    answer = "Ваши данные удалены. Чтобы снова писать в чат, авторизуйтесь повторно."
    await message.reply(answer)


async def auth_process(client, message):
    log(message, 'process')

    count = 0
    async for member in client.iter_chat_members(CHAT_ID):
        if is_authorized(member.user):
            await set_rights(client, member.user.id)
            count += 1
        else:
            await remove_rights(client, member.user.id)

    answer = "%d пользователей авторизовано." % count
    await message.reply(answer)


async def auth_stats(client, message):
    log(message, 'stats')
    answer = "%d пользователей авторизовано." % len(get_all_ids())
    await message.reply(answer)


async def auth_list(client, message):
    log(message, 'list')
    bad_users = []
    async for member in client.iter_chat_members(CHAT_ID):
        user = member.user
        if not is_authorized(user):
            bad_users.append("%s %s (%s, %d)" % (
                user.first_name,
                user.last_name,
                user.username,
                user.id
            ))

    answer = "%d пользователей не авторизовано:" % len(bad_users) + "\n".join(bad_users)
    await message.reply(answer)
