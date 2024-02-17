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


class GetAttachedStickers(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``CC5B67CC``

    Parameters:
        media (:obj:`InputStickeredMedia <team.raw.base.InputStickeredMedia>`):
            N/A

    Returns:
        List of :obj:`StickerSetCovered <team.raw.base.StickerSetCovered>`
    """

    __slots__: List[str] = ["media"]

    ID = 0xcc5b67cc
    QUALNAME = "functions.messages.GetAttachedStickers"

    def __init__(self, *, media: "raw.base.InputStickeredMedia") -> None:
        self.media = media  # InputStickeredMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAttachedStickers":
        # No flags
        
        media = TLObject.read(b)
        
        return GetAttachedStickers(media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.media.write())
        
        return b.getvalue()
