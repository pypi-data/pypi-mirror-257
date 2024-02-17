#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

RecentMeUrl = Union[raw.types.RecentMeUrlChat, raw.types.RecentMeUrlChatInvite, raw.types.RecentMeUrlStickerSet, raw.types.RecentMeUrlUnknown, raw.types.RecentMeUrlUser]


# noinspection PyRedeclaration
class RecentMeUrl:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 5 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            RecentMeUrlChat
            RecentMeUrlChatInvite
            RecentMeUrlStickerSet
            RecentMeUrlUnknown
            RecentMeUrlUser
    """

    QUALNAME = "team.raw.base.RecentMeUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/recent-me-url")
