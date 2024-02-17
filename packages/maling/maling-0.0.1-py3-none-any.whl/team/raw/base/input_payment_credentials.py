#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InputPaymentCredentials = Union[raw.types.InputPaymentCredentials, raw.types.InputPaymentCredentialsApplePay, raw.types.InputPaymentCredentialsGooglePay, raw.types.InputPaymentCredentialsSaved]


# noinspection PyRedeclaration
class InputPaymentCredentials:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 4 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InputPaymentCredentials
            InputPaymentCredentialsApplePay
            InputPaymentCredentialsGooglePay
            InputPaymentCredentialsSaved
    """

    QUALNAME = "team.raw.base.InputPaymentCredentials"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/input-payment-credentials")
