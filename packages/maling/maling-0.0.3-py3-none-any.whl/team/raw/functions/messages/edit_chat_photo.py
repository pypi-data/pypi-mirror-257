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


class EditChatPhoto(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``35DDD674``

    Parameters:
        chat_id (``int`` ``64-bit``):
            N/A

        photo (:obj:`InputChatPhoto <team.raw.base.InputChatPhoto>`):
            N/A

    Returns:
        :obj:`Updates <team.raw.base.Updates>`
    """

    __slots__: List[str] = ["chat_id", "photo"]

    ID = 0x35ddd674
    QUALNAME = "functions.messages.EditChatPhoto"

    def __init__(self, *, chat_id: int, photo: "raw.base.InputChatPhoto") -> None:
        self.chat_id = chat_id  # long
        self.photo = photo  # InputChatPhoto

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditChatPhoto":
        # No flags
        
        chat_id = Long.read(b)
        
        photo = TLObject.read(b)
        
        return EditChatPhoto(chat_id=chat_id, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.chat_id))
        
        b.write(self.photo.write())
        
        return b.getvalue()
