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


class ImportedContacts(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.contacts.ImportedContacts`.

    Details:
        - Layer: ``158``
        - ID: ``77D01C3B``

    Parameters:
        imported (List of :obj:`ImportedContact <team.raw.base.ImportedContact>`):
            N/A

        popular_invites (List of :obj:`PopularContact <team.raw.base.PopularContact>`):
            N/A

        retry_contacts (List of ``int`` ``64-bit``):
            N/A

        users (List of :obj:`User <team.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            contacts.ImportContacts
    """

    __slots__: List[str] = ["imported", "popular_invites", "retry_contacts", "users"]

    ID = 0x77d01c3b
    QUALNAME = "types.contacts.ImportedContacts"

    def __init__(self, *, imported: List["raw.base.ImportedContact"], popular_invites: List["raw.base.PopularContact"], retry_contacts: List[int], users: List["raw.base.User"]) -> None:
        self.imported = imported  # Vector<ImportedContact>
        self.popular_invites = popular_invites  # Vector<PopularContact>
        self.retry_contacts = retry_contacts  # Vector<long>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ImportedContacts":
        # No flags
        
        imported = TLObject.read(b)
        
        popular_invites = TLObject.read(b)
        
        retry_contacts = TLObject.read(b, Long)
        
        users = TLObject.read(b)
        
        return ImportedContacts(imported=imported, popular_invites=popular_invites, retry_contacts=retry_contacts, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.imported))
        
        b.write(Vector(self.popular_invites))
        
        b.write(Vector(self.retry_contacts, Long))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
