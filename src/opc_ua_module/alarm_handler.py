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

import logging
from rfc5424logging import LOG_LOCAL0, Rfc5424SysLogHandler, Rfc5424SysLogAdapter
import socket
from urllib.parse import urlparse


class AlarmHandler:

    def __init__(self, syslog_server_address, opc_server_url: str, output_socket_tcp):
        logger = logging.getLogger('opc-ua-listen')
        logger.setLevel(logging.INFO)
        socket_type = socket.SOCK_DGRAM
        self._opc_server_hostname = self._format_opc_server_hostname(opc_server_url)
        if output_socket_tcp:
            socket_type = socket.SOCK_STREAM
        handler = Rfc5424SysLogHandler(address=syslog_server_address, socktype=socket_type, facility=LOG_LOCAL0, msg_as_utf8=False)
        handler.append_nul = False
        logger.addHandler(handler)
        self._logger_adapter = Rfc5424SysLogAdapter(logger)

    def event_notification(self, event):
        content = repr(event)
        # append_nul and terminating \n are necessary for rsyslog to correctly interpret messages when they are sent over TCP
        # see issue CYB-59 and https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler.emit
        self._logger_adapter.info(f'{content}', hostname=self._opc_server_hostname, appname='OPC-UA', procid='-', msgid="alarm_event")

    def _format_opc_server_hostname(self, opc_server_url: str) -> str:
        parsed_url = urlparse(opc_server_url)
        return parsed_url.hostname
