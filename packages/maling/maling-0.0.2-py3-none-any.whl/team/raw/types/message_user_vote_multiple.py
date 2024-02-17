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


class MessageUserVoteMultiple(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.MessageUserVote`.

    Details:
        - Layer: ``158``
        - ID: ``8A65E557``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        options (List of ``bytes``):
            N/A

        date (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["user_id", "options", "date"]

    ID = 0x8a65e557
    QUALNAME = "types.MessageUserVoteMultiple"

    def __init__(self, *, user_id: int, options: List[bytes], date: int) -> None:
        self.user_id = user_id  # long
        self.options = options  # Vector<bytes>
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageUserVoteMultiple":
        # No flags
        
        user_id = Long.read(b)
        
        options = TLObject.read(b, Bytes)
        
        date = Int.read(b)
        
        return MessageUserVoteMultiple(user_id=user_id, options=options, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(Vector(self.options, Bytes))
        
        b.write(Int(self.date))
        
        return b.getvalue()
