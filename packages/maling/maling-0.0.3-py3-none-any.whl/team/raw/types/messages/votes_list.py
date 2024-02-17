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


class VotesList(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.messages.VotesList`.

    Details:
        - Layer: ``158``
        - ID: ``823F649``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        votes (List of :obj:`MessageUserVote <team.raw.base.MessageUserVote>`):
            N/A

        users (List of :obj:`User <team.raw.base.User>`):
            N/A

        next_offset (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetPollVotes
    """

    __slots__: List[str] = ["count", "votes", "users", "next_offset"]

    ID = 0x823f649
    QUALNAME = "types.messages.VotesList"

    def __init__(self, *, count: int, votes: List["raw.base.MessageUserVote"], users: List["raw.base.User"], next_offset: Optional[str] = None) -> None:
        self.count = count  # int
        self.votes = votes  # Vector<MessageUserVote>
        self.users = users  # Vector<User>
        self.next_offset = next_offset  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "VotesList":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        votes = TLObject.read(b)
        
        users = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        return VotesList(count=count, votes=votes, users=users, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.votes))
        
        b.write(Vector(self.users))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        return b.getvalue()
