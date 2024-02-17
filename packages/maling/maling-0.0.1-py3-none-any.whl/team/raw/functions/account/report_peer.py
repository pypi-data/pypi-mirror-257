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


class ReportPeer(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``C5BA3D86``

    Parameters:
        peer (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

        reason (:obj:`ReportReason <team.raw.base.ReportReason>`):
            N/A

        message (``str``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "reason", "message"]

    ID = 0xc5ba3d86
    QUALNAME = "functions.account.ReportPeer"

    def __init__(self, *, peer: "raw.base.InputPeer", reason: "raw.base.ReportReason", message: str) -> None:
        self.peer = peer  # InputPeer
        self.reason = reason  # ReportReason
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportPeer":
        # No flags
        
        peer = TLObject.read(b)
        
        reason = TLObject.read(b)
        
        message = String.read(b)
        
        return ReportPeer(peer=peer, reason=reason, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.reason.write())
        
        b.write(String(self.message))
        
        return b.getvalue()
