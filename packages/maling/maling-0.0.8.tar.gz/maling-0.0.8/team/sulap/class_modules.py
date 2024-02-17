from importlib import import_module
from math import ceil
from sys import version as pyver

from modular import import_modular
from pyrogram import __version__ as pyrover
from pyrogram.types import InlineKeyboardButton
from pytgcalls.__version__ import __version__ as pytgver

from .class_mix import *

CMD_HELP = {}
from . import LOGGER, udB


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({})".format(
                        prefix, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    line = 3
    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    max_num_pages = ceil(len(pairs) / line)
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⪻",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "⪼",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs


async def refresh_modules():
    LOGGER.info(f"Importing All Modules...")
    modxx = import_modular()
    for modx in modxx:
        imported_module = import_module(f"modular.{modx}")
        if hasattr(imported_module, "__modles__") and imported_module.__modles__:
            imported_module.__modles__ = imported_module.__modles__
            if hasattr(imported_module, "__help__") and imported_module.__help__:
                CMD_HELP[imported_module.__modles__.replace(" ", "_").lower()] = (
                    imported_module
                )
    await bot.send_message(
        udB.get_logger(user.me.id),
        f"""
<b>Userbot Successfully Deploy !!</b>

<b>Modules : {len(CMD_HELP)}</b>
<b>Python : {pyver.split()[0]}</b>
<b>Pyrogram : {pyrover}</b>
<b>Pytgcalls : {pytgver}</b>
<b>Prefixes : {udB.get_pref(user.me.id)}</b>
""",
    )
