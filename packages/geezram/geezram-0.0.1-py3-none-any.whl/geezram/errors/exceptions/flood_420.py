# geezram - Telegram MTProto API Client Library for Python.
# Copyright (C) 2022-2023 Iskandar <https://github.com/darmazi>
#
# This file is part of geezram.
#
# geezram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# geezram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with geezram.  If not, see <http://www.gnu.org/licenses/>.

from ..rpc_error import RPCError


class Flood(RPCError):
    """Flood"""
    CODE = 420
    """``int``: RPC Error Code"""
    NAME = __doc__


class TwoFaConfirmWait(Flood):
    """Tungguin sampe {value} detik diperlukan karena akun ini aktif dan dilindungi oleh kata sandi 2FA"""
    ID = "2FA_CONFIRM_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FloodTestPhoneWait(Flood):
    """Tungguin sampe {value} detik diperlukan di server pengujian"""
    ID = "FLOOD_TEST_PHONE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FloodWait(Flood):
    """Tungguin sampe {value} detik dulu ngentot"""
    ID = "FLOOD_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SlowmodeWait(Flood):
    """Tungguin sampe {value} detik dulu, baru bisa kirim pesan di obrolan ini."""
    ID = "SLOWMODE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TakeoutInitDelay(Flood):
    """Anda harus mengonfirmasi permintaan ekspor data menggunakan salah satu perangkat seluler Anda atau menunggu {value} detik"""
    ID = "TAKEOUT_INIT_DELAY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


