#  geezram - Telegram MTProto API Client Library for Python.
#  Copyright (C) 2022-2023 Iskandar <https://github.com/darmazi>
#
#  This file is part of geezram.
#
#  geezram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  geezram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with geezram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from geezram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from geezram.raw.core import TLObject
from geezram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class PageBlockBlockquote(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.PageBlock`.

    Details:
        - Layer: ``148``
        - ID: ``263D7C26``

    Parameters:
        text (:obj:`RichText <geezram.raw.base.RichText>`):
            N/A

        caption (:obj:`RichText <geezram.raw.base.RichText>`):
            N/A

    """

    __slots__: List[str] = ["text", "caption"]

    ID = 0x263d7c26
    QUALNAME = "types.PageBlockBlockquote"

    def __init__(self, *, text: "raw.base.RichText", caption: "raw.base.RichText") -> None:
        self.text = text  # RichText
        self.caption = caption  # RichText

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockBlockquote":
        # No flags
        
        text = TLObject.read(b)
        
        caption = TLObject.read(b)
        
        return PageBlockBlockquote(text=text, caption=caption)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(self.caption.write())
        
        return b.getvalue()
