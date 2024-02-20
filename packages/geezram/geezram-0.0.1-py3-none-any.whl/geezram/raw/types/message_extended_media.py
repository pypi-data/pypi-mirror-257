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


class MessageExtendedMedia(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.MessageExtendedMedia`.

    Details:
        - Layer: ``148``
        - ID: ``EE479C64``

    Parameters:
        media (:obj:`MessageMedia <geezram.raw.base.MessageMedia>`):
            N/A

    """

    __slots__: List[str] = ["media"]

    ID = 0xee479c64
    QUALNAME = "types.MessageExtendedMedia"

    def __init__(self, *, media: "raw.base.MessageMedia") -> None:
        self.media = media  # MessageMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageExtendedMedia":
        # No flags
        
        media = TLObject.read(b)
        
        return MessageExtendedMedia(media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.media.write())
        
        return b.getvalue()
