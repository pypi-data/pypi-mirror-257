#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

LangPackLanguage = Union[raw.types.LangPackLanguage]


# noinspection PyRedeclaration
class LangPackLanguage:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            LangPackLanguage

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            langpack.GetLanguages
            langpack.GetLanguage
    """

    QUALNAME = "team.raw.base.LangPackLanguage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/lang-pack-language")
