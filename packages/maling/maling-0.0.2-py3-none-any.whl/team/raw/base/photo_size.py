#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

PhotoSize = Union[raw.types.PhotoCachedSize, raw.types.PhotoPathSize, raw.types.PhotoSize, raw.types.PhotoSizeEmpty, raw.types.PhotoSizeProgressive, raw.types.PhotoStrippedSize]


# noinspection PyRedeclaration
class PhotoSize:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            PhotoCachedSize
            PhotoPathSize
            PhotoSize
            PhotoSizeEmpty
            PhotoSizeProgressive
            PhotoStrippedSize
    """

    QUALNAME = "team.raw.base.PhotoSize"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/photo-size")
