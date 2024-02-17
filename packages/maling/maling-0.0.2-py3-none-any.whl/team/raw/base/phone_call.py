#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

PhoneCall = Union[raw.types.PhoneCall, raw.types.PhoneCallAccepted, raw.types.PhoneCallDiscarded, raw.types.PhoneCallEmpty, raw.types.PhoneCallRequested, raw.types.PhoneCallWaiting]


# noinspection PyRedeclaration
class PhoneCall:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            PhoneCall
            PhoneCallAccepted
            PhoneCallDiscarded
            PhoneCallEmpty
            PhoneCallRequested
            PhoneCallWaiting
    """

    QUALNAME = "team.raw.base.PhoneCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/phone-call")
