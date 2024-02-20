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


class InvokeAfterMsgs(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``148``
        - ID: ``3DC4B4F0``

    Parameters:
        msg_ids (List of ``int`` ``64-bit``):
            N/A

        query (Any function from :obj:`~geezram.raw.functions`):
            N/A

    Returns:
        Any object from :obj:`~geezram.raw.types`
    """

    __slots__: List[str] = ["msg_ids", "query"]

    ID = 0x3dc4b4f0
    QUALNAME = "functions.InvokeAfterMsgs"

    def __init__(self, *, msg_ids: List[int], query: TLObject) -> None:
        self.msg_ids = msg_ids  # Vector<long>
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvokeAfterMsgs":
        # No flags
        
        msg_ids = TLObject.read(b, Long)
        
        query = TLObject.read(b)
        
        return InvokeAfterMsgs(msg_ids=msg_ids, query=query)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.msg_ids, Long))
        
        b.write(self.query.write())
        
        return b.getvalue()
