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


class FeaturedStickersNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.messages.FeaturedStickers`.

    Details:
        - Layer: ``158``
        - ID: ``C6DC0C66``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetFeaturedStickers
            messages.GetOldFeaturedStickers
            messages.GetFeaturedEmojiStickers
    """

    __slots__: List[str] = ["count"]

    ID = 0xc6dc0c66
    QUALNAME = "types.messages.FeaturedStickersNotModified"

    def __init__(self, *, count: int) -> None:
        self.count = count  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "FeaturedStickersNotModified":
        # No flags
        
        count = Int.read(b)
        
        return FeaturedStickersNotModified(count=count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        return b.getvalue()
