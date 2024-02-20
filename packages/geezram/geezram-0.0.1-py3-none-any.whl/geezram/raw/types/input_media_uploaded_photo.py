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


class InputMediaUploadedPhoto(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.InputMedia`.

    Details:
        - Layer: ``148``
        - ID: ``1E287D04``

    Parameters:
        file (:obj:`InputFile <geezram.raw.base.InputFile>`):
            N/A

        stickers (List of :obj:`InputDocument <geezram.raw.base.InputDocument>`, *optional*):
            N/A

        ttl_seconds (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["file", "stickers", "ttl_seconds"]

    ID = 0x1e287d04
    QUALNAME = "types.InputMediaUploadedPhoto"

    def __init__(self, *, file: "raw.base.InputFile", stickers: Optional[List["raw.base.InputDocument"]] = None, ttl_seconds: Optional[int] = None) -> None:
        self.file = file  # InputFile
        self.stickers = stickers  # flags.0?Vector<InputDocument>
        self.ttl_seconds = ttl_seconds  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaUploadedPhoto":
        
        flags = Int.read(b)
        
        file = TLObject.read(b)
        
        stickers = TLObject.read(b) if flags & (1 << 0) else []
        
        ttl_seconds = Int.read(b) if flags & (1 << 1) else None
        return InputMediaUploadedPhoto(file=file, stickers=stickers, ttl_seconds=ttl_seconds)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.stickers else 0
        flags |= (1 << 1) if self.ttl_seconds is not None else 0
        b.write(Int(flags))
        
        b.write(self.file.write())
        
        if self.stickers is not None:
            b.write(Vector(self.stickers))
        
        if self.ttl_seconds is not None:
            b.write(Int(self.ttl_seconds))
        
        return b.getvalue()
