#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

SuggestedShortName = Union[raw.types.stickers.SuggestedShortName]


# noinspection PyRedeclaration
class SuggestedShortName:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            stickers.SuggestedShortName

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            stickers.SuggestShortName
    """

    QUALNAME = "team.raw.base.stickers.SuggestedShortName"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/suggested-short-name")
