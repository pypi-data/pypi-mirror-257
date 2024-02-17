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


class PhotosSlice(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.photos.Photos`.

    Details:
        - Layer: ``158``
        - ID: ``15051F54``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        photos (List of :obj:`Photo <team.raw.base.Photo>`):
            N/A

        users (List of :obj:`User <team.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            photos.GetUserPhotos
    """

    __slots__: List[str] = ["count", "photos", "users"]

    ID = 0x15051f54
    QUALNAME = "types.photos.PhotosSlice"

    def __init__(self, *, count: int, photos: List["raw.base.Photo"], users: List["raw.base.User"]) -> None:
        self.count = count  # int
        self.photos = photos  # Vector<Photo>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhotosSlice":
        # No flags
        
        count = Int.read(b)
        
        photos = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PhotosSlice(count=count, photos=photos, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.photos))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
