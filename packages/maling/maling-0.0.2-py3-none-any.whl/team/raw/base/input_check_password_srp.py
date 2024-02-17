#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InputCheckPasswordSRP = Union[raw.types.InputCheckPasswordEmpty, raw.types.InputCheckPasswordSRP]


# noinspection PyRedeclaration
class InputCheckPasswordSRP:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InputCheckPasswordEmpty
            InputCheckPasswordSRP
    """

    QUALNAME = "team.raw.base.InputCheckPasswordSRP"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/input-check-password-srp")
