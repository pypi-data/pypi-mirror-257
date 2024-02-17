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


class CanPurchasePremium(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``9FC19EB6``

    Parameters:
        purpose (:obj:`InputStorePaymentPurpose <team.raw.base.InputStorePaymentPurpose>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["purpose"]

    ID = 0x9fc19eb6
    QUALNAME = "functions.payments.CanPurchasePremium"

    def __init__(self, *, purpose: "raw.base.InputStorePaymentPurpose") -> None:
        self.purpose = purpose  # InputStorePaymentPurpose

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CanPurchasePremium":
        # No flags
        
        purpose = TLObject.read(b)
        
        return CanPurchasePremium(purpose=purpose)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.purpose.write())
        
        return b.getvalue()
