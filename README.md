# OPC-UA Log Fetcher

## License

OPC-UA Log Fetcher

Copyright (C) 2023 Airbus CyberSecurity SAS

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

### Third-party software usage

This program uses the following software to run:

| Software | Version | Copyright | License |
|-|-|-|-|
| opcua-asyncio (asyncua) | ^1.0.0 | 2023 FreeOpcUa  | LGPL-3.0-or-later |
| rfc5424-logging-handler | ^1.4.3 | 2017 Joris Beckers | BSD-3-Clause |


## Command cheatsheet

This project requires poetry (https://python-poetry.org/docs/#installing-with-the-official-installer).

### Install dependencies
```
poetry install
```

### Set the VERSION number variable
```
VERSION=$(poetry version --short) && echo ${VERSION}
```

### Build

Build the python package:
```
poetry build
```
The package will be in directory `dist`.
Then build the docker:
```
docker build --file docker/Dockerfile --tag opc-ua-log-fetcher:${VERSION} .
```

#### Archive the docker image
```
docker save opc-ua-log-fetcher:${VERSION} | gzip > opc-ua-log-fetcher-${VERSION}.docker.tar.gz
```

To import the image:
```
docker load --input opc-ua-log-fetcher-${VERSION}.docker.tar.gz
```

### Execute
First start your server.

To execute the fetcher:
```
docker run --rm --network host --volume /dev/log:/dev/log opc-ua-log-fetcher:${VERSION}
```

To execute the script with poetry:
```
poetry run opc-ua-listen
poetry run opc-ua-listen --help
```

#### Security

1. no security at all
   ```
   poetry run opc-ua-listen
   ```
2. username authentication, no security
   ```
   poetry run opc-ua-listen --url opc.tcp://username@localhost:4840/freeopcua/server/
   ```
3. no authentication/security-policy SignAndEncrypt
   ```
   poetry run opc-ua-listen --private-key ./poc/certificates/peer-private-key-example-1.pem --certificate ./poc/certificates/peer-certificate-example-1.der --server-certificate ./poc/certificates/server-certificate-example.der
   ```
4. username authentication, certificates checks and encryption
   ```
   poetry run opc-ua-listen --url opc.tcp://username@localhost:4840/freeopcua/server/ --private-key ./poc/certificates/peer-private-key-example-1.pem --certificate ./poc/certificates/peer-certificate-example-1.der --server-certificate ./poc/certificates/server-certificate-example.der
   ```

### Publish a new version

```
git tag -s ${VERSION} -m "Release ${VERSION}"
git push origin --tags
```
