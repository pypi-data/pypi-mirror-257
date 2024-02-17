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


class NotificationSoundNone(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.NotificationSound`.

    Details:
        - Layer: ``158``
        - ID: ``6F0C34DF``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x6f0c34df
    QUALNAME = "types.NotificationSoundNone"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "NotificationSoundNone":
        # No flags
        
        return NotificationSoundNone()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
