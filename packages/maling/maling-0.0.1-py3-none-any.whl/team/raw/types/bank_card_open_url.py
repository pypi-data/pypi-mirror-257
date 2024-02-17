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


class BankCardOpenUrl(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.BankCardOpenUrl`.

    Details:
        - Layer: ``158``
        - ID: ``F568028A``

    Parameters:
        url (``str``):
            N/A

        name (``str``):
            N/A

    """

    __slots__: List[str] = ["url", "name"]

    ID = 0xf568028a
    QUALNAME = "types.BankCardOpenUrl"

    def __init__(self, *, url: str, name: str) -> None:
        self.url = url  # string
        self.name = name  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BankCardOpenUrl":
        # No flags
        
        url = String.read(b)
        
        name = String.read(b)
        
        return BankCardOpenUrl(url=url, name=name)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(String(self.name))
        
        return b.getvalue()
