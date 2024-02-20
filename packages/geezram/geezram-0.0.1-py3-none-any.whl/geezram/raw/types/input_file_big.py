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


class InputFileBig(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.InputFile`.

    Details:
        - Layer: ``148``
        - ID: ``FA4F0BB5``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        parts (``int`` ``32-bit``):
            N/A

        name (``str``):
            N/A

    """

    __slots__: List[str] = ["id", "parts", "name"]

    ID = 0xfa4f0bb5
    QUALNAME = "types.InputFileBig"

    def __init__(self, *, id: int, parts: int, name: str) -> None:
        self.id = id  # long
        self.parts = parts  # int
        self.name = name  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputFileBig":
        # No flags
        
        id = Long.read(b)
        
        parts = Int.read(b)
        
        name = String.read(b)
        
        return InputFileBig(id=id, parts=parts, name=name)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Int(self.parts))
        
        b.write(String(self.name))
        
        return b.getvalue()
