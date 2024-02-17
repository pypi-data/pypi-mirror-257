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


class ReadParticipantDate(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.ReadParticipantDate`.

    Details:
        - Layer: ``158``
        - ID: ``4A4FF172``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetMessageReadParticipants
    """

    __slots__: List[str] = ["user_id", "date"]

    ID = 0x4a4ff172
    QUALNAME = "types.ReadParticipantDate"

    def __init__(self, *, user_id: int, date: int) -> None:
        self.user_id = user_id  # long
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReadParticipantDate":
        # No flags
        
        user_id = Long.read(b)
        
        date = Int.read(b)
        
        return ReadParticipantDate(user_id=user_id, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(Int(self.date))
        
        return b.getvalue()
