# -*- coding: utf-8 -*-

from authlib.integrations.requests_client import OAuth2Session
from config import CHAT_ID, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_AUTH_ENDPOINT
from utils.logs import log
from utils.rights import set_rights, remove_rights
from utils.tokens import create_state
from utils.users import get_all_ids, get_username, delete_user


async def auth_start(client, message):
    log(message, 'start')

    username = get_username(message.from_user.id)
    if username is None:
        await auth_link(client, message)
        return

    await set_rights(client, message.from_user.id)
    answer = '''
Вы уже авторизованы как [%s](https://ru.wikipedia.org/wiki/User:%s).
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
    tg_ids = get_all_ids()

    async for member in client.iter_chat_members(CHAT_ID):
        tg_id = member.user.id
        if tg_id in tg_ids:
            await set_rights(client, tg_id)
        else:
            await remove_rights(client, tg_id)

    answer = "%d пользователей авторизовано." % len(tg_ids)
    await message.reply(answer)
