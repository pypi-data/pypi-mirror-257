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


class ExportedChatInvite(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~geezram.raw.base.messages.ExportedChatInvite`.

    Details:
        - Layer: ``148``
        - ID: ``1871BE50``

    Parameters:
        invite (:obj:`ExportedChatInvite <geezram.raw.base.ExportedChatInvite>`):
            N/A

        users (List of :obj:`User <geezram.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: geezram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetExportedChatInvite
            messages.EditExportedChatInvite
    """

    __slots__: List[str] = ["invite", "users"]

    ID = 0x1871be50
    QUALNAME = "types.messages.ExportedChatInvite"

    def __init__(self, *, invite: "raw.base.ExportedChatInvite", users: List["raw.base.User"]) -> None:
        self.invite = invite  # ExportedChatInvite
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedChatInvite":
        # No flags
        
        invite = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ExportedChatInvite(invite=invite, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.invite.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
