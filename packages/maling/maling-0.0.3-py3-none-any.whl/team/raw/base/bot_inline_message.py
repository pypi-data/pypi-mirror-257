#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

BotInlineMessage = Union[raw.types.BotInlineMessageMediaAuto, raw.types.BotInlineMessageMediaContact, raw.types.BotInlineMessageMediaGeo, raw.types.BotInlineMessageMediaInvoice, raw.types.BotInlineMessageMediaVenue, raw.types.BotInlineMessageText]


# noinspection PyRedeclaration
class BotInlineMessage:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            BotInlineMessageMediaAuto
            BotInlineMessageMediaContact
            BotInlineMessageMediaGeo
            BotInlineMessageMediaInvoice
            BotInlineMessageMediaVenue
            BotInlineMessageText
    """

    QUALNAME = "team.raw.base.BotInlineMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/bot-inline-message")
