#  geezram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of geezram.
#
#  geezram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  geezram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with geezram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import geezram
from geezram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~geezram.types.InlineQueryResultCachedAudio`
    - :obj:`~geezram.types.InlineQueryResultCachedDocument`
    - :obj:`~geezram.types.InlineQueryResultCachedAnimation`
    - :obj:`~geezram.types.InlineQueryResultCachedPhoto`
    - :obj:`~geezram.types.InlineQueryResultCachedSticker`
    - :obj:`~geezram.types.InlineQueryResultCachedVideo`
    - :obj:`~geezram.types.InlineQueryResultCachedVoice`
    - :obj:`~geezram.types.InlineQueryResultArticle`
    - :obj:`~geezram.types.InlineQueryResultAudio`
    - :obj:`~geezram.types.InlineQueryResultContact`
    - :obj:`~geezram.types.InlineQueryResultDocument`
    - :obj:`~geezram.types.InlineQueryResultAnimation`
    - :obj:`~geezram.types.InlineQueryResultLocation`
    - :obj:`~geezram.types.InlineQueryResultPhoto`
    - :obj:`~geezram.types.InlineQueryResultVenue`
    - :obj:`~geezram.types.InlineQueryResultVideo`
    - :obj:`~geezram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "geezram.Client"):
        pass
