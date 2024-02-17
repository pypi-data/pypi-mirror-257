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


class MessageMediaWebPage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.MessageMedia`.

    Details:
        - Layer: ``158``
        - ID: ``A32DD600``

    Parameters:
        webpage (:obj:`WebPage <team.raw.base.WebPage>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPagePreview
            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["webpage"]

    ID = 0xa32dd600
    QUALNAME = "types.MessageMediaWebPage"

    def __init__(self, *, webpage: "raw.base.WebPage") -> None:
        self.webpage = webpage  # WebPage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaWebPage":
        # No flags
        
        webpage = TLObject.read(b)
        
        return MessageMediaWebPage(webpage=webpage)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.webpage.write())
        
        return b.getvalue()
