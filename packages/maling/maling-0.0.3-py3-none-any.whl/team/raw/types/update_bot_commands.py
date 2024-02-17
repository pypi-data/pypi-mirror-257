#  Library Team

from io import BytesIO

from team.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from team.raw.core import TLObject
from team import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class UpdateBotCommands(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``4D712F2E``

    Parameters:
        peer (:obj:`Peer <team.raw.base.Peer>`):
            N/A

        bot_id (``int`` ``64-bit``):
            N/A

        commands (List of :obj:`BotCommand <team.raw.base.BotCommand>`):
            N/A

    """

    __slots__: List[str] = ["peer", "bot_id", "commands"]

    ID = 0x4d712f2e
    QUALNAME = "types.UpdateBotCommands"

    def __init__(self, *, peer: "raw.base.Peer", bot_id: int, commands: List["raw.base.BotCommand"]) -> None:
        self.peer = peer  # Peer
        self.bot_id = bot_id  # long
        self.commands = commands  # Vector<BotCommand>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotCommands":
        # No flags
        
        peer = TLObject.read(b)
        
        bot_id = Long.read(b)
        
        commands = TLObject.read(b)
        
        return UpdateBotCommands(peer=peer, bot_id=bot_id, commands=commands)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Long(self.bot_id))
        
        b.write(Vector(self.commands))
        
        return b.getvalue()
