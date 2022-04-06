# -*- coding: utf-8 -*-

from authlib.integrations.requests_client import OAuth2Session
from config import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_AUTH_ENDPOINT
from utils.logs import log
from utils.rights import set_rights, remove_rights
from utils.tokens import create_state
from utils.users import get_username, delete_user


async def auth_start(client, message):
    log(message, 'start')

    username = get_username(message.from_user.id)
    if username is None:
        await auth_link(client, message)
        return

    set_rights(client, message.from_user.id)
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
    remove_rights(message.from_user.id)

    answer = "Ваши данные удалены."
    # answer = "Ваши данные удалены. Доступ к закрытым чатам отозван."
    await message.reply_chat_action(answer, disable_web_page_preview=True)
