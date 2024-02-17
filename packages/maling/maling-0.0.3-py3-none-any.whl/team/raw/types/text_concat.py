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


class TextConcat(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.RichText`.

    Details:
        - Layer: ``158``
        - ID: ``7E6260D7``

    Parameters:
        texts (List of :obj:`RichText <team.raw.base.RichText>`):
            N/A

    """

    __slots__: List[str] = ["texts"]

    ID = 0x7e6260d7
    QUALNAME = "types.TextConcat"

    def __init__(self, *, texts: List["raw.base.RichText"]) -> None:
        self.texts = texts  # Vector<RichText>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextConcat":
        # No flags
        
        texts = TLObject.read(b)
        
        return TextConcat(texts=texts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.texts))
        
        return b.getvalue()
