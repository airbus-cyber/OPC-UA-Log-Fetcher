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

FROM python:3-alpine

ARG MODULE_VERSION
COPY opc_ua_module-${MODULE_VERSION}-py3-none-any.whl opc_ua_module-${MODULE_VERSION}-py3-none-any.whl
RUN pip install opc_ua_module-${MODULE_VERSION}-py3-none-any.whl && rm opc_ua_module-${MODULE_VERSION}-py3-none-any.whl

HEALTHCHECK CMD [ `netstat | grep ESTABLISHED | wc -l` -eq 2 ]

ENTRYPOINT ["opc-ua-listen"]
