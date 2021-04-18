#!/usr/bin/env python3
"""
Ublox-Api session package

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
from contextlib import asynccontextmanager

# Third Party
from aiohttp import ClientSession, TCPConnector
import orjson

# ----------------------------------------------------------------------------


@asynccontextmanager
async def get_ublox_api_session() -> ClientSession:
    """Async Context manager to get a session to communicate with UbloxApi"""
    connector = TCPConnector(limit=2, ssl=False, ttl_dns_cache=300)
    session = ClientSession(
        connector=connector,
        json_serialize=lambda x: orjson.dumps(x).decode(),
        raise_for_status=True,
        connector_owner=True,
    )
    try:
        yield session
    finally:
        await session.close()
