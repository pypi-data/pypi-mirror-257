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


class WallPapers(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.account.WallPapers`.

    Details:
        - Layer: ``148``
        - ID: ``CDC3858C``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        wallpapers (List of :obj:`WallPaper <geezram.raw.base.WallPaper>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: geezram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetWallPapers
    """

    __slots__: List[str] = ["hash", "wallpapers"]

    ID = 0xcdc3858c
    QUALNAME = "types.account.WallPapers"

    def __init__(self, *, hash: int, wallpapers: List["raw.base.WallPaper"]) -> None:
        self.hash = hash  # long
        self.wallpapers = wallpapers  # Vector<WallPaper>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WallPapers":
        # No flags
        
        hash = Long.read(b)
        
        wallpapers = TLObject.read(b)
        
        return WallPapers(hash=hash, wallpapers=wallpapers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.wallpapers))
        
        return b.getvalue()
