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


class MessageActionChatEditPhoto(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.MessageAction`.

    Details:
        - Layer: ``158``
        - ID: ``7FCB13A8``

    Parameters:
        photo (:obj:`Photo <team.raw.base.Photo>`):
            N/A

    """

    __slots__: List[str] = ["photo"]

    ID = 0x7fcb13a8
    QUALNAME = "types.MessageActionChatEditPhoto"

    def __init__(self, *, photo: "raw.base.Photo") -> None:
        self.photo = photo  # Photo

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionChatEditPhoto":
        # No flags
        
        photo = TLObject.read(b)
        
        return MessageActionChatEditPhoto(photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.photo.write())
        
        return b.getvalue()
