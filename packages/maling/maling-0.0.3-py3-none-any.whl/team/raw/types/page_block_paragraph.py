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


class PageBlockParagraph(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.PageBlock`.

    Details:
        - Layer: ``158``
        - ID: ``467A0766``

    Parameters:
        text (:obj:`RichText <team.raw.base.RichText>`):
            N/A

    """

    __slots__: List[str] = ["text"]

    ID = 0x467a0766
    QUALNAME = "types.PageBlockParagraph"

    def __init__(self, *, text: "raw.base.RichText") -> None:
        self.text = text  # RichText

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockParagraph":
        # No flags
        
        text = TLObject.read(b)
        
        return PageBlockParagraph(text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        return b.getvalue()
