#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InputWallPaper = Union[raw.types.InputWallPaper, raw.types.InputWallPaperNoFile, raw.types.InputWallPaperSlug]


# noinspection PyRedeclaration
class InputWallPaper:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InputWallPaper
            InputWallPaperNoFile
            InputWallPaperSlug
    """

    QUALNAME = "team.raw.base.InputWallPaper"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/input-wall-paper")
