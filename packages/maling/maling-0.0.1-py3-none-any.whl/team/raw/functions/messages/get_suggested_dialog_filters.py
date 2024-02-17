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


class GetSuggestedDialogFilters(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``A29CD42C``

    Parameters:
        No parameters required.

    Returns:
        List of :obj:`DialogFilterSuggested <team.raw.base.DialogFilterSuggested>`
    """

    __slots__: List[str] = []

    ID = 0xa29cd42c
    QUALNAME = "functions.messages.GetSuggestedDialogFilters"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSuggestedDialogFilters":
        # No flags
        
        return GetSuggestedDialogFilters()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
