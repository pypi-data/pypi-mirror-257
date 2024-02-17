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


class MessageViews(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.messages.MessageViews`.

    Details:
        - Layer: ``158``
        - ID: ``B6C4F543``

    Parameters:
        views (List of :obj:`MessageViews <team.raw.base.MessageViews>`):
            N/A

        chats (List of :obj:`Chat <team.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <team.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetMessagesViews
    """

    __slots__: List[str] = ["views", "chats", "users"]

    ID = 0xb6c4f543
    QUALNAME = "types.messages.MessageViews"

    def __init__(self, *, views: List["raw.base.MessageViews"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.views = views  # Vector<MessageViews>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageViews":
        # No flags
        
        views = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return MessageViews(views=views, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.views))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
