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


class ExportedChatlistInvite(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.chatlists.ExportedChatlistInvite`.

    Details:
        - Layer: ``158``
        - ID: ``10E6E3A6``

    Parameters:
        filter (:obj:`DialogFilter <team.raw.base.DialogFilter>`):
            N/A

        invite (:obj:`ExportedChatlistInvite <team.raw.base.ExportedChatlistInvite>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            chatlists.ExportChatlistInvite
    """

    __slots__: List[str] = ["filter", "invite"]

    ID = 0x10e6e3a6
    QUALNAME = "types.chatlists.ExportedChatlistInvite"

    def __init__(self, *, filter: "raw.base.DialogFilter", invite: "raw.base.ExportedChatlistInvite") -> None:
        self.filter = filter  # DialogFilter
        self.invite = invite  # ExportedChatlistInvite

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedChatlistInvite":
        # No flags
        
        filter = TLObject.read(b)
        
        invite = TLObject.read(b)
        
        return ExportedChatlistInvite(filter=filter, invite=invite)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.filter.write())
        
        b.write(self.invite.write())
        
        return b.getvalue()
