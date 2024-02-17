################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from . import LOGGER, udB
from Mix import user, bot

async def check_logger():
    LOGGER.info(f"Check Grup Log User...")
    if udB.get_logger(user.me.id) is not None:
        return
    
    await user.logger_grup()
    xx =  await user.get_grup()
    ff = int(xx.id)
    await user.promote_chat_member(ff, bot.me.username)
    udB.set_logger(user.me.id, int(xx.id))
    