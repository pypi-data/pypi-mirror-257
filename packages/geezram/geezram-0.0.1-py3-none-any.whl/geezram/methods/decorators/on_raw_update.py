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

from typing import Callable

import geezram


class OnRawUpdate:
    def on_raw_update(
        self=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling raw updates.

        This does the same thing as :meth:`~geezram.Client.add_handler` using the
        :obj:`~geezram.handlers.RawUpdateHandler`.

        Parameters:
            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, geezram.Client):
                self.add_handler(geezram.handlers.RawUpdateHandler(func), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        geezram.handlers.RawUpdateHandler(func),
                        group
                    )
                )

            return func

        return decorator
