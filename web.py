from authlib.integrations.requests_client import OAuth2Session
from bottle import redirect, request, response, route, run, template

from config import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_ACCESS_TOKEN_ENDPOINT, OAUTH_RESOURCE_PROFILE_ENDPOINT
from utils.logs import log_web
from utils.tokens import mark_state_used, get_by_state
from utils.users import create_user, get_username


@route('/')
def index():
    return ""


@route('/callback')
def callback():
    log_web('callback', '', request.url)

    state = request.query['state']
    tg_id, tg_name = get_by_state(state)
    if tg_id is None:
        log_web('bad_state', state, request.url)
        redirect("/failure")

    mark_state_used(state)

    auth_client = OAuth2Session(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET)
    try:
        token = auth_client.fetch_token(
            OAUTH_ACCESS_TOKEN_ENDPOINT,
            authorization_response=request.url,
            grant_type='authorization_code',
        )

        auth_client = OAuth2Session(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, token=token)
        resp = auth_client.get(OAUTH_RESOURCE_PROFILE_ENDPOINT)
        wiki_name = resp.json()['username']

        create_user(tg_id, tg_name, wiki_name)
        log_web('success', wiki_name, resp.text, tg_id)

        redirect("/success")
    except Exception as err:
        log_web('error', 'callback', err)
        log_web('failure', '', request.url)
        redirect("/failure")


@route('/success')
def success():
    try:
        file = open('web/success.html', mode='r')
        html = file.read()
        file.close()

        return template(html)
    except Exception as err:
        log_web('error', 'success', err)
        log_web('failure', '', request.url)
        redirect("/failure")


@route('/failure')
def failure():
    file = open('web/failure.html', mode='r')
    html = file.read()
    file.close()

    return template(html)


run(host='localhost', port=8080, debug=True)