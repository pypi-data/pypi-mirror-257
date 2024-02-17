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


class JsonObject(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.JSONValue`.

    Details:
        - Layer: ``158``
        - ID: ``99C1D49D``

    Parameters:
        value (List of :obj:`JSONObjectValue <team.raw.base.JSONObjectValue>`):
            N/A

    """

    __slots__: List[str] = ["value"]

    ID = 0x99c1d49d
    QUALNAME = "types.JsonObject"

    def __init__(self, *, value: List["raw.base.JSONObjectValue"]) -> None:
        self.value = value  # Vector<JSONObjectValue>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JsonObject":
        # No flags
        
        value = TLObject.read(b)
        
        return JsonObject(value=value)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.value))
        
        return b.getvalue()
