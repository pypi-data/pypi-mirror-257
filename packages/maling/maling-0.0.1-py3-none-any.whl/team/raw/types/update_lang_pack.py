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


class UpdateLangPack(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``56022F4D``

    Parameters:
        difference (:obj:`LangPackDifference <team.raw.base.LangPackDifference>`):
            N/A

    """

    __slots__: List[str] = ["difference"]

    ID = 0x56022f4d
    QUALNAME = "types.UpdateLangPack"

    def __init__(self, *, difference: "raw.base.LangPackDifference") -> None:
        self.difference = difference  # LangPackDifference

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateLangPack":
        # No flags
        
        difference = TLObject.read(b)
        
        return UpdateLangPack(difference=difference)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.difference.write())
        
        return b.getvalue()
