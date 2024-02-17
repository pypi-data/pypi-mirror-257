#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

Themes = Union[raw.types.account.Themes, raw.types.account.ThemesNotModified]


# noinspection PyRedeclaration
class Themes:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            account.Themes
            account.ThemesNotModified

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetThemes
            account.GetChatThemes
    """

    QUALNAME = "team.raw.base.account.Themes"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/themes")
