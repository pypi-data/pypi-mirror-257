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


class Reactions(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.messages.Reactions`.

    Details:
        - Layer: ``158``
        - ID: ``EAFDF716``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        reactions (List of :obj:`Reaction <team.raw.base.Reaction>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetTopReactions
            messages.GetRecentReactions
    """

    __slots__: List[str] = ["hash", "reactions"]

    ID = 0xeafdf716
    QUALNAME = "types.messages.Reactions"

    def __init__(self, *, hash: int, reactions: List["raw.base.Reaction"]) -> None:
        self.hash = hash  # long
        self.reactions = reactions  # Vector<Reaction>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Reactions":
        # No flags
        
        hash = Long.read(b)
        
        reactions = TLObject.read(b)
        
        return Reactions(hash=hash, reactions=reactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.reactions))
        
        return b.getvalue()
