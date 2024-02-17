#  Library Team

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from team import raw
from team.raw.core import TLObject

MessageUserVote = Union[raw.types.MessageUserVote, raw.types.MessageUserVoteInputOption, raw.types.MessageUserVoteMultiple]


# noinspection PyRedeclaration
class MessageUserVote:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: team.raw.types

        .. autosummary::
            :nosignatures:

            MessageUserVote
            MessageUserVoteInputOption
            MessageUserVoteMultiple
    """

    QUALNAME = "team.raw.base.MessageUserVote"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.team.org/telegram/base/message-user-vote")
