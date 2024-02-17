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


class SendScreenshotNotification(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``C97DF020``

    Parameters:
        peer (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

        reply_to_msg_id (``int`` ``32-bit``):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

    Returns:
        :obj:`Updates <team.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "reply_to_msg_id", "random_id"]

    ID = 0xc97df020
    QUALNAME = "functions.messages.SendScreenshotNotification"

    def __init__(self, *, peer: "raw.base.InputPeer", reply_to_msg_id: int, random_id: int) -> None:
        self.peer = peer  # InputPeer
        self.reply_to_msg_id = reply_to_msg_id  # int
        self.random_id = random_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendScreenshotNotification":
        # No flags
        
        peer = TLObject.read(b)
        
        reply_to_msg_id = Int.read(b)
        
        random_id = Long.read(b)
        
        return SendScreenshotNotification(peer=peer, reply_to_msg_id=reply_to_msg_id, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.reply_to_msg_id))
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
