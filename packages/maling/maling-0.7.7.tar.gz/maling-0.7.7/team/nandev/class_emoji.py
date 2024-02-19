################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from .class_log import LOGGER
from .database import udB
import asyncio
from Mix import user

def Emojii():
    emo = {}

    ping_var = udB.get_var(user.me.id, "emo_ping") or "5269563867305879894"
    emo_ping = str(ping_var)

    pong_var = udB.get_var(user.me.id, "emo_pong") or "6183961455436498818"
    emo_pong = str(pong_var)

    proses_var = udB.get_var(user.me.id, "emo_proses") or "5974326532670230199"
    emo_proses = str(proses_var)

    sukses_var = udB.get_var(user.me.id, "emo_sukses") or "5021905410089550576"
    emo_sukses = str(sukses_var)

    gagal_var = udB.get_var(user.me.id, "emo_gagal") or "5019523782004441717"
    emo_gagal = str(gagal_var)

    profil_var = udB.get_var(user.me.id, "emo_profil") or "5373012449597335010"
    emo_profil = str(profil_var)

    alive_var = udB.get_var(user.me.id, "emo_alive") or "4934091419288601395"
    emo_alive = str(alive_var)

    warn_var = udB.get_var(user.me.id, "emo_warn") or "6172475875368373616"
    emo_warn = str(warn_var)

    block_var = udB.get_var(user.me.id, "emo_block") or "5240241223632954241"
    emo_block = str(block_var)

    def format_emoji(emoji_id, emoji):
        return f"<emoji id={emoji_id}>{emoji}</emoji>"

    emo["ping"] = lambda: format_emoji(emo_ping, "🏓")
    emo["pong"] = lambda: format_emoji(emo_pong, "🥵")
    emo["proses"] = lambda: format_emoji(emo_proses, "🔄")
    emo["sukses"] = lambda: format_emoji(emo_sukses, "✅")
    emo["gagal"] = lambda: format_emoji(emo_gagal, "❌")
    emo["profil"] = lambda: format_emoji(emo_profil, "👤")
    emo["alive"] = lambda: format_emoji(emo_alive, "⭐")
    emo["warn"] = lambda: format_emoji(emo_warn, "❗️")
    emo["block"] = lambda: format_emoji(emo_block, "🚫")

    return emo


async def load_emo():
    eping = "🏓"
    ping_id = "<emoji id=5269563867305879894>🏓</emoji>"
    epong = "🥵"
    pong_id = "<emoji id=6183961455436498818>🥵</emoji>"
    eproses = "🔄"
    proses_id = "<emoji id=6113844439292054570>🔄</emoji>"
    egagal = "❌"
    gagal_id = "<emoji id=6113872536968104754>❌</emoji>"
    esukses = "✅"
    sukses_id = "<emoji id=6113647841459047673>✅</emoji>"
    eprofil = "👤"
    profil_id = "<emoji id=5373012449597335010>👤</emoji>"
    ealive = "⭐"
    alive_id = "<emoji id=6127272826341690178>⭐</emoji>"
    ewarn = "❗️"
    warn_id = "<emoji id=6172475875368373616>❗️</emoji>"
    eblock = "🚫"
    block_id = "<emoji id=5240241223632954241>🚫</emoji>"
    a = udB.get_var(user.me.id, "emo_ping")
    b = udB.get_var(user.me.id, "emo_pong")
    c = udB.get_var(user.me.id, "emo_proses")
    d = udB.get_var(user.me.id, "emo_gagal")
    e = udB.get_var(user.me.id, "emo_sukses")
    f = udB.get_var(user.me.id, "emo_profil")
    g = udB.get_var(user.me.id, "emo_alive")
    h = udB.get_var(user.me.id, "emo_warn")
    i = udB.get_var(user.me.id, "emo_block")
    uprem = user.me.is_premium
    if uprem == True:
        if (a, b, c, d, e, f, g, h, i) is not None:
            return
        else:
            udB.set_var(user.me.id, "emo_ping", ping_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_pong", pong_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_proses", proses_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_gagal", gagal_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_sukses", sukses_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_profil", profil_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_alive", alive_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_warn", warn_id)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_block", block_id)
    elif uprem == False:
        if (a, b, c, d, e, f, g, h, i) is not None:
            return
        else:
            udB.set_var(user.me.id, "emo_ping", eping)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_pong", epong)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_proses", eproses)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_gagal", egagal)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_sukses", esukses)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_profil", eprofil)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_alive", ealive)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_warn", ewarn)
            await asyncio.sleep(0.5)
            udB.set_var(user.me.id, "emo_block", eblock)

