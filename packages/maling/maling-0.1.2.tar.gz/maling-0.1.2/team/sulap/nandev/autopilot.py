################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio
from .database import udB
from Mix import user
from .class_ubot import LOGGER
from random import randint
from os import execvp
from sys import executable


async def autobot():
    
    if udB.get_token(user.me.id) is not None:
        return
    LOGGER.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    gw = user.me
    name = gw.first_name + " Asisstant"
    if gw.username:
        username = gw.username + "_bot"
    else:
        username = "mix_" + (str(gw.id))[5:] + "_bot"
    bf = "@BotFather"
    await user.unblock_user(bf)
    await user.send_message(bf, "/start")
    await asyncio.sleep(1)
    await user.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, "Alright, a new bot.", limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone is None or "20 bots" in isdone:
        LOGGER.error(
            "Tolong buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan mulai ulang saya."
        )
        import sys

        sys.exit(1)
    await user.send_message(bf, name)
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Good."):
        await user.send_message(bf, username)
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "mix_" + (str(gw.id))[6:] + str(ran) + "_bot"
        await user.send_message(bf, username)
        await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
         isdone = None
    token = None
    for k in isdone.split("HTTP API:"):
      token = k.split("\n")[1]
    if token:
        udB.set_token(user.me.id, token)
        await enable_inline(user, username)
        with open(".env", "a") as f:
            f.write(f"bot_token={token}\n")
        LOGGER.info(
            f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
        )
        execvp(executable, [executable, "-m", "Mix"])
    else:
        LOGGER.info(
            "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
        )

        import sys

        sys.exit(1)

"""
async def autopilot():

    channel = udB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await user.get_entity(channel)
        except BaseException as err:
            LOGGER.exception(err)
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:

        async def _save(exc):
            udB._cache["LOG_CHANNEL"] = user.me.id
            await asst.send_message(
                user.me.id, f"Gagal Membuat Saluran Log karena {exc}.."
            )

        if user._bot:
            msg_ = "'LOG_CHANNEL' tidak ditemukan! Tambahkan untuk digunakan 'BOTMODE'"
            LOGGER.error(msg_)
            return await _save(msg_)
        LOGGER.info("Membuat Saluran Log untuk Anda!")
        try:
            r = await user(
                CreateChannelRequest(
                    title="Naya-Userbot LOGGER()",
                    about="Ini adalah grup LOGGER() dari Naya-Userbot\nJangan keluar dari grup LOGGER() ini\nPowered By @KynanSupport",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError as er:
            LOGGER.critical(
                "Anda Berada di Terlalu Banyak Saluran & Grup, Tinggalkan beberapa dan Mulai Ulang Bot"
            )
            return await _save(str(er))
        except BaseException as er:
            LOGGER.exception(er)
            LOGGER.info(
                "Ada yang Salah, Buat Grup dan atur idnya di config var LOG_CHANNEL."
            )

            return await _save(str(er))
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", channel)
    assistant = True
    try:
        await user.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await user(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGGER.info("Kesalahan saat Menambahkan Asisten ke Saluran Log")
            LOGGER.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGGER.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGGER.info("Terjadi error saat mendapatkan saluran Log dari Asisten")
            LOGGER.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await user(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGGER.info(
                    "Gagal mempromosikan 'Bot Asisten' di 'Log Channel' karena 'Hak Istimewa Admin'"
                )
            except BaseException as er:
                LOGGER.info(
                    "Terjadi kesalahan saat mempromosikan asisten di Log Channel.."
                )
                LOGGER.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo = await download_file(
            "https://graph.org/file/60408fea8439e6702674d.jpg", "logo.jpg"
        )
        ll = await user.upload_file(photo)
        try:
            await user(EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll)))
        except BaseException as er:
            LOGGER.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, user, udB

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGGER.info("Menyesuaikan Bot Asisten di @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not user.me.username:
            sir = user.me.first_name
        else:
            sir = f"@{user.me.username}"
        file = random.choice(
            [
                "https://graph.org/file/60408fea8439e6702674d.jpg",
                "resources/extras/logo.jpg",
            ]
        )
        if not os.path.exists(file):
            file = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Penyesuaian Otomatis** Dimulai @Botfather"
        )
        await asyncio.sleep(1)
        await user.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await user.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await user.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGGER.info("Error while trying to customise assistant, skipping...")
            return
        await user.send_message("botfather", UL)
        await asyncio.sleep(1)
        await user.send_file("botfather", file)
        await asyncio.sleep(2)
        await user.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await user.send_message("botfather", UL)
        await asyncio.sleep(1)
        await user.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await user.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await user.send_message("botfather", UL)
        await asyncio.sleep(1)
        await user.send_message(
            "botfather",
            f"✨ Powerful Naya-Userbot Assistant  ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @KynanSupport ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("Completed **Auto Customisation** at @BotFather.")
        if rem:
            os.remove(file)
        LOGGER.info("Customisation Done")
    except Exception as e:
        LOGGER.exception(e)
"""
        
async def enable_inline(user, username):
    bf = "BotFather"
    await user.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await user.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await user.send_message(bf, "Search")
