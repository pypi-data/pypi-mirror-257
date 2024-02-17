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


class GetChatlistUpdates(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``89419521``

    Parameters:
        chatlist (:obj:`InputChatlist <team.raw.base.InputChatlist>`):
            N/A

    Returns:
        :obj:`chatlists.ChatlistUpdates <team.raw.base.chatlists.ChatlistUpdates>`
    """

    __slots__: List[str] = ["chatlist"]

    ID = 0x89419521
    QUALNAME = "functions.chatlists.GetChatlistUpdates"

    def __init__(self, *, chatlist: "raw.base.InputChatlist") -> None:
        self.chatlist = chatlist  # InputChatlist

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetChatlistUpdates":
        # No flags
        
        chatlist = TLObject.read(b)
        
        return GetChatlistUpdates(chatlist=chatlist)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chatlist.write())
        
        return b.getvalue()
