#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

LangPackString = Union[raw.types.LangPackString, raw.types.LangPackStringDeleted, raw.types.LangPackStringPluralized]


# noinspection PyRedeclaration
class LangPackString:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            LangPackString
            LangPackStringDeleted
            LangPackStringPluralized

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            langpack.GetStrings
    """

    QUALNAME = "team.raw.base.LangPackString"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/lang-pack-string")
