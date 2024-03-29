# This file is part of OPC-UA Log Fetcher.
#
# Copyright (C) 2023 Airbus CyberSecurity SAS
#
# OPC-UA Log Fetcher is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# OPC-UA Log Fetcher is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# OPC-UA Log Fetcher. If not, see <https://www.gnu.org/licenses/>.

import asyncio
import time
from asyncua import Client
from asyncua.ua import ObjectIds
from opc_ua_module.alarm_handler import AlarmHandler
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256


class AlarmCapture:

    def __init__(self, url, syslog_address, output_socket_tcp, certificate, private_key, server_certificate):
        self._client = Client(url=url)
        self._alarm_handler = AlarmHandler(syslog_address, url, output_socket_tcp)
        self._certificate = certificate
        self._private_key = private_key
        self._server_certificate = server_certificate

    async def _set_security(self):
        if not self._private_key:
            return
        if not self._certificate:
            return
        if not self._server_certificate:
            return
        await self._client.set_security(
            SecurityPolicyBasic256Sha256,
            self._certificate,
            self._private_key,
            server_certificate=self._server_certificate
        )

    async def _connect(self):
        while True:
            try:
                await self._client.connect()
                return
            except OSError as e:
                print(f'Connection to server failed with with exception: \'{e}\'')
                wait_duration = 10
                print(f'Trying again in {wait_duration} seconds...')
                time.sleep(wait_duration)

    async def _capture(self):
        await self._set_security()
        await self._connect()
        try:
            subscription = await self._client.create_subscription(1000, self._alarm_handler)
            handle = await subscription.subscribe_alarms_and_conditions(self._client.nodes.server,
                                                                        ObjectIds.AlarmConditionType)

            try:
                while True:
                    await asyncio.sleep(100)
            # note: the finally is necessary in case of Keyboard interrupt
            finally:
                await subscription.unsubscribe(handle)
        finally:
            await self._client.disconnect()

    def capture(self):
        asyncio.run(self._capture())
