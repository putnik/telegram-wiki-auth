# -*- coding: utf-8 -*-

def log(client, message):
    # print(message)
    out = "%d # %s (%d): \"%s\"" % (
        message.chat.id,
        message.from_user.username,
        message.from_user.id,
        message.text,
    )
    print(out)
