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


class TextImage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.RichText`.

    Details:
        - Layer: ``158``
        - ID: ``81CCF4F``

    Parameters:
        document_id (``int`` ``64-bit``):
            N/A

        w (``int`` ``32-bit``):
            N/A

        h (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["document_id", "w", "h"]

    ID = 0x81ccf4f
    QUALNAME = "types.TextImage"

    def __init__(self, *, document_id: int, w: int, h: int) -> None:
        self.document_id = document_id  # long
        self.w = w  # int
        self.h = h  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextImage":
        # No flags
        
        document_id = Long.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        return TextImage(document_id=document_id, w=w, h=h)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.document_id))
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        return b.getvalue()
