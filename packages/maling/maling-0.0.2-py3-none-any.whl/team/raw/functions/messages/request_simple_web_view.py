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


class RequestSimpleWebView(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``299BEC8E``

    Parameters:
        bot (:obj:`InputUser <team.raw.base.InputUser>`):
            N/A

        url (``str``):
            N/A

        platform (``str``):
            N/A

        from_switch_webview (``bool``, *optional*):
            N/A

        theme_params (:obj:`DataJSON <team.raw.base.DataJSON>`, *optional*):
            N/A

    Returns:
        :obj:`SimpleWebViewResult <team.raw.base.SimpleWebViewResult>`
    """

    __slots__: List[str] = ["bot", "url", "platform", "from_switch_webview", "theme_params"]

    ID = 0x299bec8e
    QUALNAME = "functions.messages.RequestSimpleWebView"

    def __init__(self, *, bot: "raw.base.InputUser", url: str, platform: str, from_switch_webview: Optional[bool] = None, theme_params: "raw.base.DataJSON" = None) -> None:
        self.bot = bot  # InputUser
        self.url = url  # string
        self.platform = platform  # string
        self.from_switch_webview = from_switch_webview  # flags.1?true
        self.theme_params = theme_params  # flags.0?DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestSimpleWebView":
        
        flags = Int.read(b)
        
        from_switch_webview = True if flags & (1 << 1) else False
        bot = TLObject.read(b)
        
        url = String.read(b)
        
        theme_params = TLObject.read(b) if flags & (1 << 0) else None
        
        platform = String.read(b)
        
        return RequestSimpleWebView(bot=bot, url=url, platform=platform, from_switch_webview=from_switch_webview, theme_params=theme_params)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.from_switch_webview else 0
        flags |= (1 << 0) if self.theme_params is not None else 0
        b.write(Int(flags))
        
        b.write(self.bot.write())
        
        b.write(String(self.url))
        
        if self.theme_params is not None:
            b.write(self.theme_params.write())
        
        b.write(String(self.platform))
        
        return b.getvalue()
