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


class TranslateResult(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.messages.TranslatedText`.

    Details:
        - Layer: ``158``
        - ID: ``33DB32F8``

    Parameters:
        result (List of :obj:`TextWithEntities <team.raw.base.TextWithEntities>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.TranslateText
    """

    __slots__: List[str] = ["result"]

    ID = 0x33db32f8
    QUALNAME = "types.messages.TranslateResult"

    def __init__(self, *, result: List["raw.base.TextWithEntities"]) -> None:
        self.result = result  # Vector<TextWithEntities>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TranslateResult":
        # No flags
        
        result = TLObject.read(b)
        
        return TranslateResult(result=result)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.result))
        
        return b.getvalue()
