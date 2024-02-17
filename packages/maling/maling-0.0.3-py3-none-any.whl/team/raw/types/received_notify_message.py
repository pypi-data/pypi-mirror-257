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


class ReceivedNotifyMessage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.ReceivedNotifyMessage`.

    Details:
        - Layer: ``158``
        - ID: ``A384B779``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        flags (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.ReceivedMessages
    """

    __slots__: List[str] = ["id", "flags"]

    ID = 0xa384b779
    QUALNAME = "types.ReceivedNotifyMessage"

    def __init__(self, *, id: int, flags: int) -> None:
        self.id = id  # int
        self.flags = flags  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReceivedNotifyMessage":
        # No flags
        
        id = Int.read(b)
        
        flags = Int.read(b)
        
        return ReceivedNotifyMessage(id=id, flags=flags)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Int(self.flags))
        
        return b.getvalue()
