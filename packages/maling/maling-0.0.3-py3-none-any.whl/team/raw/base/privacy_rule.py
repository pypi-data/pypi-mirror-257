#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

PrivacyRule = Union[raw.types.PrivacyValueAllowAll, raw.types.PrivacyValueAllowChatParticipants, raw.types.PrivacyValueAllowContacts, raw.types.PrivacyValueAllowUsers, raw.types.PrivacyValueDisallowAll, raw.types.PrivacyValueDisallowChatParticipants, raw.types.PrivacyValueDisallowContacts, raw.types.PrivacyValueDisallowUsers]


# noinspection PyRedeclaration
class PrivacyRule:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 8 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            PrivacyValueAllowAll
            PrivacyValueAllowChatParticipants
            PrivacyValueAllowContacts
            PrivacyValueAllowUsers
            PrivacyValueDisallowAll
            PrivacyValueDisallowChatParticipants
            PrivacyValueDisallowContacts
            PrivacyValueDisallowUsers
    """

    QUALNAME = "team.raw.base.PrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/privacy-rule")
