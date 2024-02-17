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


class JsonArray(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.JSONValue`.

    Details:
        - Layer: ``158``
        - ID: ``F7444763``

    Parameters:
        value (List of :obj:`JSONValue <team.raw.base.JSONValue>`):
            N/A

    """

    __slots__: List[str] = ["value"]

    ID = 0xf7444763
    QUALNAME = "types.JsonArray"

    def __init__(self, *, value: List["raw.base.JSONValue"]) -> None:
        self.value = value  # Vector<JSONValue>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JsonArray":
        # No flags
        
        value = TLObject.read(b)
        
        return JsonArray(value=value)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.value))
        
        return b.getvalue()
