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


class InputDocumentEmpty(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.InputDocument`.

    Details:
        - Layer: ``158``
        - ID: ``72F0EAAE``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x72f0eaae
    QUALNAME = "types.InputDocumentEmpty"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputDocumentEmpty":
        # No flags
        
        return InputDocumentEmpty()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
