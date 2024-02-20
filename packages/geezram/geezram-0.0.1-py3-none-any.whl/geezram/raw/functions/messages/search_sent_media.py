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


class SearchSentMedia(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``148``
        - ID: ``107E31A0``

    Parameters:
        q (``str``):
            N/A

        filter (:obj:`MessagesFilter <geezram.raw.base.MessagesFilter>`):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`messages.Messages <geezram.raw.base.messages.Messages>`
    """

    __slots__: List[str] = ["q", "filter", "limit"]

    ID = 0x107e31a0
    QUALNAME = "functions.messages.SearchSentMedia"

    def __init__(self, *, q: str, filter: "raw.base.MessagesFilter", limit: int) -> None:
        self.q = q  # string
        self.filter = filter  # MessagesFilter
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchSentMedia":
        # No flags
        
        q = String.read(b)
        
        filter = TLObject.read(b)
        
        limit = Int.read(b)
        
        return SearchSentMedia(q=q, filter=filter, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(self.filter.write())
        
        b.write(Int(self.limit))
        
        return b.getvalue()
