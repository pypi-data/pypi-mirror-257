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


class UpdateMessageID(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.Update`.

    Details:
        - Layer: ``148``
        - ID: ``4E90BFD6``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["id", "random_id"]

    ID = 0x4e90bfd6
    QUALNAME = "types.UpdateMessageID"

    def __init__(self, *, id: int, random_id: int) -> None:
        self.id = id  # int
        self.random_id = random_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateMessageID":
        # No flags
        
        id = Int.read(b)
        
        random_id = Long.read(b)
        
        return UpdateMessageID(id=id, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
