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


class PageBlockAudio(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.PageBlock`.

    Details:
        - Layer: ``148``
        - ID: ``804361EA``

    Parameters:
        audio_id (``int`` ``64-bit``):
            N/A

        caption (:obj:`PageCaption <geezram.raw.base.PageCaption>`):
            N/A

    """

    __slots__: List[str] = ["audio_id", "caption"]

    ID = 0x804361ea
    QUALNAME = "types.PageBlockAudio"

    def __init__(self, *, audio_id: int, caption: "raw.base.PageCaption") -> None:
        self.audio_id = audio_id  # long
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockAudio":
        # No flags
        
        audio_id = Long.read(b)
        
        caption = TLObject.read(b)
        
        return PageBlockAudio(audio_id=audio_id, caption=caption)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.audio_id))
        
        b.write(self.caption.write())
        
        return b.getvalue()
