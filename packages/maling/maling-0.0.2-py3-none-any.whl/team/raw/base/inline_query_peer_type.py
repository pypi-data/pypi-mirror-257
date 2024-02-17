#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InlineQueryPeerType = Union[raw.types.InlineQueryPeerTypeBotPM, raw.types.InlineQueryPeerTypeBroadcast, raw.types.InlineQueryPeerTypeChat, raw.types.InlineQueryPeerTypeMegagroup, raw.types.InlineQueryPeerTypePM, raw.types.InlineQueryPeerTypeSameBotPM]


# noinspection PyRedeclaration
class InlineQueryPeerType:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InlineQueryPeerTypeBotPM
            InlineQueryPeerTypeBroadcast
            InlineQueryPeerTypeChat
            InlineQueryPeerTypeMegagroup
            InlineQueryPeerTypePM
            InlineQueryPeerTypeSameBotPM
    """

    QUALNAME = "team.raw.base.InlineQueryPeerType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/inline-query-peer-type")
