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


class Unblock(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``BEA65D50``

    Parameters:
        id (:obj:`InputPeer <team.raw.base.InputPeer>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["id"]

    ID = 0xbea65d50
    QUALNAME = "functions.contacts.Unblock"

    def __init__(self, *, id: "raw.base.InputPeer") -> None:
        self.id = id  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Unblock":
        # No flags
        
        id = TLObject.read(b)
        
        return Unblock(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
