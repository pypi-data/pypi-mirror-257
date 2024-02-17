#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

LoginToken = Union[raw.types.auth.LoginToken, raw.types.auth.LoginTokenMigrateTo, raw.types.auth.LoginTokenSuccess]


# noinspection PyRedeclaration
class LoginToken:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            auth.LoginToken
            auth.LoginTokenMigrateTo
            auth.LoginTokenSuccess

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            auth.ExportLoginToken
            auth.ImportLoginToken
    """

    QUALNAME = "team.raw.base.auth.LoginToken"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/login-token")
