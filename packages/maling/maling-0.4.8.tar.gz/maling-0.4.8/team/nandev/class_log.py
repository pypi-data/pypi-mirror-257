################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from os import execvp
from sys import executable
import logging

class ConnectionHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        for X in ["Connection lost", "OSError"]:
            if X in record.getMessage():
                execvp(executable, [executable, "-m", "Mix"])


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)

LOGS = logging.getLogger()

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

def LOGG(name: str) -> logging.Logger:
    return logging.getLogger(name)
    
LOGGER = LOGG("Mix-Userbot")