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


class StatsURL(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.StatsURL`.

    Details:
        - Layer: ``158``
        - ID: ``47A971E0``

    Parameters:
        url (``str``):
            N/A

    """

    __slots__: List[str] = ["url"]

    ID = 0x47a971e0
    QUALNAME = "types.StatsURL"

    def __init__(self, *, url: str) -> None:
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StatsURL":
        # No flags
        
        url = String.read(b)
        
        return StatsURL(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        return b.getvalue()
