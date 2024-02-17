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


class CheckPassword(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``D18B4D16``

    Parameters:
        password (:obj:`InputCheckPasswordSRP <team.raw.base.InputCheckPasswordSRP>`):
            N/A

    Returns:
        :obj:`auth.Authorization <team.raw.base.auth.Authorization>`
    """

    __slots__: List[str] = ["password"]

    ID = 0xd18b4d16
    QUALNAME = "functions.auth.CheckPassword"

    def __init__(self, *, password: "raw.base.InputCheckPasswordSRP") -> None:
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckPassword":
        # No flags
        
        password = TLObject.read(b)
        
        return CheckPassword(password=password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.password.write())
        
        return b.getvalue()
