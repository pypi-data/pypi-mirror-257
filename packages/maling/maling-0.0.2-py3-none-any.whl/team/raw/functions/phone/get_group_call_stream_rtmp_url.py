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


class GetGroupCallStreamRtmpUrl(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``DEB3ABBF``

    Parameters:
        peer (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

        revoke (``bool``):
            N/A

    Returns:
        :obj:`phone.GroupCallStreamRtmpUrl <team.raw.base.phone.GroupCallStreamRtmpUrl>`
    """

    __slots__: List[str] = ["peer", "revoke"]

    ID = 0xdeb3abbf
    QUALNAME = "functions.phone.GetGroupCallStreamRtmpUrl"

    def __init__(self, *, peer: "raw.base.InputPeer", revoke: bool) -> None:
        self.peer = peer  # InputPeer
        self.revoke = revoke  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetGroupCallStreamRtmpUrl":
        # No flags
        
        peer = TLObject.read(b)
        
        revoke = Bool.read(b)
        
        return GetGroupCallStreamRtmpUrl(peer=peer, revoke=revoke)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bool(self.revoke))
        
        return b.getvalue()
