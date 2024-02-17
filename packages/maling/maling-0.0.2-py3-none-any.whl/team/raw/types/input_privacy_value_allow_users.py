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


class InputPrivacyValueAllowUsers(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.InputPrivacyRule`.

    Details:
        - Layer: ``158``
        - ID: ``131CC67F``

    Parameters:
        users (List of :obj:`InputUser <team.raw.base.InputUser>`):
            N/A

    """

    __slots__: List[str] = ["users"]

    ID = 0x131cc67f
    QUALNAME = "types.InputPrivacyValueAllowUsers"

    def __init__(self, *, users: List["raw.base.InputUser"]) -> None:
        self.users = users  # Vector<InputUser>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyValueAllowUsers":
        # No flags
        
        users = TLObject.read(b)
        
        return InputPrivacyValueAllowUsers(users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.users))
        
        return b.getvalue()
