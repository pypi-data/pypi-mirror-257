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


class ForumTopicDeleted(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.ForumTopic`.

    Details:
        - Layer: ``158``
        - ID: ``23F109B``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["id"]

    ID = 0x23f109b
    QUALNAME = "types.ForumTopicDeleted"

    def __init__(self, *, id: int) -> None:
        self.id = id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForumTopicDeleted":
        # No flags
        
        id = Int.read(b)
        
        return ForumTopicDeleted(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        return b.getvalue()
