#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InputBotInlineMessage = Union[raw.types.InputBotInlineMessageGame, raw.types.InputBotInlineMessageMediaAuto, raw.types.InputBotInlineMessageMediaContact, raw.types.InputBotInlineMessageMediaGeo, raw.types.InputBotInlineMessageMediaInvoice, raw.types.InputBotInlineMessageMediaVenue, raw.types.InputBotInlineMessageText]


# noinspection PyRedeclaration
class InputBotInlineMessage:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 7 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InputBotInlineMessageGame
            InputBotInlineMessageMediaAuto
            InputBotInlineMessageMediaContact
            InputBotInlineMessageMediaGeo
            InputBotInlineMessageMediaInvoice
            InputBotInlineMessageMediaVenue
            InputBotInlineMessageText
    """

    QUALNAME = "team.raw.base.InputBotInlineMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/input-bot-inline-message")
