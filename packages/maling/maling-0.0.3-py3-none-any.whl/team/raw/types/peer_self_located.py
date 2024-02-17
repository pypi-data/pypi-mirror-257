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


class PeerSelfLocated(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.PeerLocated`.

    Details:
        - Layer: ``158``
        - ID: ``F8EC284B``

    Parameters:
        expires (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["expires"]

    ID = 0xf8ec284b
    QUALNAME = "types.PeerSelfLocated"

    def __init__(self, *, expires: int) -> None:
        self.expires = expires  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerSelfLocated":
        # No flags
        
        expires = Int.read(b)
        
        return PeerSelfLocated(expires=expires)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.expires))
        
        return b.getvalue()
