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


class EmojiStatusUntil(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.EmojiStatus`.

    Details:
        - Layer: ``148``
        - ID: ``FA30A8C7``

    Parameters:
        document_id (``int`` ``64-bit``):
            N/A

        until (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["document_id", "until"]

    ID = 0xfa30a8c7
    QUALNAME = "types.EmojiStatusUntil"

    def __init__(self, *, document_id: int, until: int) -> None:
        self.document_id = document_id  # long
        self.until = until  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatusUntil":
        # No flags
        
        document_id = Long.read(b)
        
        until = Int.read(b)
        
        return EmojiStatusUntil(document_id=document_id, until=until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.document_id))
        
        b.write(Int(self.until))
        
        return b.getvalue()
