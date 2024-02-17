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


class EmojiKeyword(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.EmojiKeyword`.

    Details:
        - Layer: ``158``
        - ID: ``D5B3B9F9``

    Parameters:
        keyword (``str``):
            N/A

        emoticons (List of ``str``):
            N/A

    """

    __slots__: List[str] = ["keyword", "emoticons"]

    ID = 0xd5b3b9f9
    QUALNAME = "types.EmojiKeyword"

    def __init__(self, *, keyword: str, emoticons: List[str]) -> None:
        self.keyword = keyword  # string
        self.emoticons = emoticons  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiKeyword":
        # No flags
        
        keyword = String.read(b)
        
        emoticons = TLObject.read(b, String)
        
        return EmojiKeyword(keyword=keyword, emoticons=emoticons)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.keyword))
        
        b.write(Vector(self.emoticons, String))
        
        return b.getvalue()
