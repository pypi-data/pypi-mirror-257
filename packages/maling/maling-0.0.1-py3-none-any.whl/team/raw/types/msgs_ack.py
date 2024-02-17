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


class MsgsAck(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.MsgsAck`.

    Details:
        - Layer: ``158``
        - ID: ``62D6B459``

    Parameters:
        msg_ids (List of ``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["msg_ids"]

    ID = 0x62d6b459
    QUALNAME = "types.MsgsAck"

    def __init__(self, *, msg_ids: List[int]) -> None:
        self.msg_ids = msg_ids  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MsgsAck":
        # No flags
        
        msg_ids = TLObject.read(b, Long)
        
        return MsgsAck(msg_ids=msg_ids)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.msg_ids, Long))
        
        return b.getvalue()
