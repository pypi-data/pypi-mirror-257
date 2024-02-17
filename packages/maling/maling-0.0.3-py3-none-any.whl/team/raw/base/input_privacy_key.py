#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

InputPrivacyKey = Union[raw.types.InputPrivacyKeyAddedByPhone, raw.types.InputPrivacyKeyChatInvite, raw.types.InputPrivacyKeyForwards, raw.types.InputPrivacyKeyPhoneCall, raw.types.InputPrivacyKeyPhoneNumber, raw.types.InputPrivacyKeyPhoneP2P, raw.types.InputPrivacyKeyProfilePhoto, raw.types.InputPrivacyKeyStatusTimestamp, raw.types.InputPrivacyKeyVoiceMessages]


# noinspection PyRedeclaration
class InputPrivacyKey:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 9 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            InputPrivacyKeyAddedByPhone
            InputPrivacyKeyChatInvite
            InputPrivacyKeyForwards
            InputPrivacyKeyPhoneCall
            InputPrivacyKeyPhoneNumber
            InputPrivacyKeyPhoneP2P
            InputPrivacyKeyProfilePhoto
            InputPrivacyKeyStatusTimestamp
            InputPrivacyKeyVoiceMessages
    """

    QUALNAME = "team.raw.base.InputPrivacyKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/input-privacy-key")
