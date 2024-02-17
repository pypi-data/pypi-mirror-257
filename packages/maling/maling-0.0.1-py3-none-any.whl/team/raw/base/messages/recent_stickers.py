#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

RecentStickers = Union[raw.types.messages.RecentStickers, raw.types.messages.RecentStickersNotModified]


# noinspection PyRedeclaration
class RecentStickers:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            messages.RecentStickers
            messages.RecentStickersNotModified

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetRecentStickers
    """

    QUALNAME = "team.raw.base.messages.RecentStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/recent-stickers")
