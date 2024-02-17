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


class PageBlockSlideshow(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.PageBlock`.

    Details:
        - Layer: ``158``
        - ID: ``31F9590``

    Parameters:
        items (List of :obj:`PageBlock <team.raw.base.PageBlock>`):
            N/A

        caption (:obj:`PageCaption <team.raw.base.PageCaption>`):
            N/A

    """

    __slots__: List[str] = ["items", "caption"]

    ID = 0x31f9590
    QUALNAME = "types.PageBlockSlideshow"

    def __init__(self, *, items: List["raw.base.PageBlock"], caption: "raw.base.PageCaption") -> None:
        self.items = items  # Vector<PageBlock>
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockSlideshow":
        # No flags
        
        items = TLObject.read(b)
        
        caption = TLObject.read(b)
        
        return PageBlockSlideshow(items=items, caption=caption)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.items))
        
        b.write(self.caption.write())
        
        return b.getvalue()
