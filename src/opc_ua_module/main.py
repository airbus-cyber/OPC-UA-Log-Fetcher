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

from argparse import ArgumentParser
from opc_ua_module.alarm_capture import AlarmCapture
import sys

_DEFAULT_SERVER_URL = 'opc.tcp://localhost:4840'
_DEFAULT_SYSLOG_ADDRESS = '/dev/log'


class Main:

    def __init__(self):
        self._parser = ArgumentParser(description='Airbus OPC UA Alarm listener')
        self._parser.add_argument('-u', '--url', default=_DEFAULT_SERVER_URL,
                                  help=f'URL of the OPC UA server to connect to. Default to {_DEFAULT_SERVER_URL}')
        self._parser.add_argument('-o', '--output', default=_DEFAULT_SYSLOG_ADDRESS,
                                  help=f'Address of the syslog output. Either host:port, or a path. Default to {_DEFAULT_SYSLOG_ADDRESS}')
        self._parser.add_argument('--tcp-output', action='store_true', help='Choose syslog socket to be tcp rather than defaut udp')
        self._parser.add_argument('--private-key', help='Path to the private key (.pem)')
        self._parser.add_argument('--certificate', help='Path to the certificate (.der)')
        self._parser.add_argument('--server-certificate', help='Path to the server certificate (.der)')

    def _parse_syslog_output(self, output):
        if ':' not in output:
            return output
        [host, port] = output.split(':', 1)
        return (host, int(port))

    def run(self, arguments):
        try:
            arguments = self._parser.parse_args(arguments[1:])
            syslog_address = self._parse_syslog_output(arguments.output)
            client = AlarmCapture(arguments.url, syslog_address, arguments.tcp_output,
                                  arguments.certificate, arguments.private_key, arguments.server_certificate)
            client.capture()
        except KeyboardInterrupt:
            pass
        # TODO error cases to handle
        #      ConnectionRefusedError here!!!!! when the server url is incorrect
        #      Value error on --output 'localhost:toto'
        #      OSError Bad file descriptor error on --output '/toto'


def run():
    main = Main()
    main.run(sys.argv)
