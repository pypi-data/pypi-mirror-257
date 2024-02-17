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


class SendBotRequestedPeer(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``FE38D01B``

    Parameters:
        peer (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        button_id (``int`` ``32-bit``):
            N/A

        requested_peer (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

    Returns:
        :obj:`Updates <team.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "msg_id", "button_id", "requested_peer"]

    ID = 0xfe38d01b
    QUALNAME = "functions.messages.SendBotRequestedPeer"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, button_id: int, requested_peer: "raw.base.InputPeer") -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.button_id = button_id  # int
        self.requested_peer = requested_peer  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendBotRequestedPeer":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        button_id = Int.read(b)
        
        requested_peer = TLObject.read(b)
        
        return SendBotRequestedPeer(peer=peer, msg_id=msg_id, button_id=button_id, requested_peer=requested_peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.button_id))
        
        b.write(self.requested_peer.write())
        
        return b.getvalue()
