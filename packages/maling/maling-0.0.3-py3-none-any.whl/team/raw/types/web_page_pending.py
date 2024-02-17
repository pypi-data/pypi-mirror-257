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


class WebPagePending(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.WebPage`.

    Details:
        - Layer: ``158``
        - ID: ``C586DA1C``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPage
    """

    __slots__: List[str] = ["id", "date"]

    ID = 0xc586da1c
    QUALNAME = "types.WebPagePending"

    def __init__(self, *, id: int, date: int) -> None:
        self.id = id  # long
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPagePending":
        # No flags
        
        id = Long.read(b)
        
        date = Int.read(b)
        
        return WebPagePending(id=id, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Int(self.date))
        
        return b.getvalue()
