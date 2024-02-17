#  Library Team

from io import BytesIO

from team.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from team.raw.core import TLObject
from team import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GlobalPrivacySettings(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.GlobalPrivacySettings`.

    Details:
        - Layer: ``158``
        - ID: ``BEA2F424``

    Parameters:
        archive_and_mute_new_noncontact_peers (``bool``, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetGlobalPrivacySettings
            account.SetGlobalPrivacySettings
    """

    __slots__: List[str] = ["archive_and_mute_new_noncontact_peers"]

    ID = 0xbea2f424
    QUALNAME = "types.GlobalPrivacySettings"

    def __init__(self, *, archive_and_mute_new_noncontact_peers: Optional[bool] = None) -> None:
        self.archive_and_mute_new_noncontact_peers = archive_and_mute_new_noncontact_peers  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GlobalPrivacySettings":
        
        flags = Int.read(b)
        
        archive_and_mute_new_noncontact_peers = Bool.read(b) if flags & (1 << 0) else None
        return GlobalPrivacySettings(archive_and_mute_new_noncontact_peers=archive_and_mute_new_noncontact_peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.archive_and_mute_new_noncontact_peers is not None else 0
        b.write(Int(flags))
        
        if self.archive_and_mute_new_noncontact_peers is not None:
            b.write(Bool(self.archive_and_mute_new_noncontact_peers))
        
        return b.getvalue()
