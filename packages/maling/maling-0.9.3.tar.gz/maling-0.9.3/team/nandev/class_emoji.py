################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Kalo Mo Pake Ini Kode Jangan Hapus Credits Ya Nooobbb
"""
################################################################

from .class_log import LOGGER
from .database import udB
import asyncio
from Mix import user

class Emojik:
    def initialize(self):
        self.ping_var = (
            udB.get_var(user.me.id, "emo_ping") or "5269563867305879894"
        )
        self.emo_ping = int(self.ping_var)

        self.pong_var = (
            udB.get_var(user.me.id, "emo_pong") or "6183961455436498818"
        )
        self.emo_pong = (
            self.pong_var = int(self.pong_var)

        self.proses_var = (
            udB.get_var(user.me.id, "emo_proses") or "5974326532670230199"
        )
        self.emo_proses = int(self.proses_var)
            
            
        self.sukses_var = (
            udB.get_var(user.me.id, "emo_sukses") or "5021905410089550576"
        )
        self.emo_sukses = int(self.sukses_var)

        self.gagal_var = (
            udB.get_var(user.me.id, "emo_gagal") or "5019523782004441717"
        )
        self.emo_gagal = int(self.gagal_var)

        self.profil_var = (
            udB.get_var(user.me.id, "emo_profil") or "5373012449597335010"
        )
        self.emo_profil = int(self.profil_var)

        self.alive_var = (
            udB.get_var(user.me.id, "emo_alive") or "4934091419288601395"
        )
        self.emo_alive = int(self.alive_var)
        
        self.warn_var = (
            udB.get_var(user.me.id, "emo_warn") or "6172475875368373616"
        )
        self.emo_warn = int(self.warn_var)
        
        self.block_var = (
            udB.get_var(user.me.id, "emo_block") or "5240241223632954241"
        )
        self.emo_block = int(self.block_var)

    @property
    def ping(self):
        return f"<emoji id={self.emo_ping}>🏓</emoji>"

    @property
    def pong(self):
        return f"<emoji id={self.emo_pong}>🥵</emoji>"

    @property
    def proses(self):
        return f"<emoji id={self.emo_proses}>🔄</emoji>"

    @property
    def sukses(self):
        return f"<emoji id={self.emo_sukses}>✅</emoji>"

    @property
    def gagal(self):
        return f"<emoji id={self.emo_gagal}>❌</emoji>"

    @property
    def profil(self):
        return f"<emoji id={self.emo_profil}>👤</emoji>"

    @property
    def alive(self):
        return f"<emoji id={self.emo_alive}>⭐</emoji>"
            
    @property
    def warn(self):
        return f"<emoji id={self.emo_warn}>❗️</emoji>"
            
    @property
    def block(self):
        return f"<emoji id={self.emo_block}>🚫</emoji>"
            
            

"""
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

def inidia():
    emo = Emojik()
    emo.initialize()
    return emo
    
jadinih = inidia()
ping = jadinih.ping
pong = jadinih.pong
proses = jadinih.proses
sukses = jadinih.sukses
gagal = jadinih.gagal
alive = jadinih.alive
profil = jadinih.profil
warn = jadinih.warn
block = jadinih.block
"""
