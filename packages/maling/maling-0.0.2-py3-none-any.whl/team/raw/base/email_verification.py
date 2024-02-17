#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

EmailVerification = Union[raw.types.EmailVerificationApple, raw.types.EmailVerificationCode, raw.types.EmailVerificationGoogle]


# noinspection PyRedeclaration
class EmailVerification:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            EmailVerificationApple
            EmailVerificationCode
            EmailVerificationGoogle
    """

    QUALNAME = "team.raw.base.EmailVerification"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/email-verification")
