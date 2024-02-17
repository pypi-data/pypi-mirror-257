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


class ChannelAdminLogEventActionDiscardGroupCall(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``158``
        - ID: ``DB9F9140``

    Parameters:
        call (:obj:`InputGroupCall <team.raw.base.InputGroupCall>`):
            N/A

    """

    __slots__: List[str] = ["call"]

    ID = 0xdb9f9140
    QUALNAME = "types.ChannelAdminLogEventActionDiscardGroupCall"

    def __init__(self, *, call: "raw.base.InputGroupCall") -> None:
        self.call = call  # InputGroupCall

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionDiscardGroupCall":
        # No flags
        
        call = TLObject.read(b)
        
        return ChannelAdminLogEventActionDiscardGroupCall(call=call)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        return b.getvalue()
