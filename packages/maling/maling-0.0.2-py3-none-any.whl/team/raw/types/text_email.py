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


class TextEmail(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.RichText`.

    Details:
        - Layer: ``158``
        - ID: ``DE5A0DD6``

    Parameters:
        text (:obj:`RichText <team.raw.base.RichText>`):
            N/A

        email (``str``):
            N/A

    """

    __slots__: List[str] = ["text", "email"]

    ID = 0xde5a0dd6
    QUALNAME = "types.TextEmail"

    def __init__(self, *, text: "raw.base.RichText", email: str) -> None:
        self.text = text  # RichText
        self.email = email  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextEmail":
        # No flags
        
        text = TLObject.read(b)
        
        email = String.read(b)
        
        return TextEmail(text=text, email=email)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(String(self.email))
        
        return b.getvalue()
