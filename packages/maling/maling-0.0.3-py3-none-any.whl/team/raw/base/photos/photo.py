#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

Photo = Union[raw.types.photos.Photo]


# noinspection PyRedeclaration
class Photo:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            photos.Photo

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            photos.UpdateProfilePhoto
            photos.UploadProfilePhoto
            photos.UploadContactProfilePhoto
    """

    QUALNAME = "team.raw.base.photos.Photo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/photo")
