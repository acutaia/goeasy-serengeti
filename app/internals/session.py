#!/usr/bin/env python3
"""
Session package

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
from functools import lru_cache
from typing import NewType

# Third Party
from httpx import AsyncClient

# ----------------------------------------------------------------------------


@lru_cache(maxsize=1)
def get_ublox_api_session() -> AsyncClient:
    """Instantiate UbloxApiSession"""
    return AsyncClient(verify=False)


@lru_cache(maxsize=1)
def get_accounting_session() -> AsyncClient:
    """Instantiate AccountingSession"""
    return AsyncClient()


@lru_cache(maxsize=1)
def get_anonymizer_session() -> AsyncClient:
    """Instantiate AccountingSession"""
    return AsyncClient(verify=False)


def instantiate_all_sessions():
    """instantiate all sessions included in serengeti"""
    get_ublox_api_session()
    get_accounting_session()
    get_anonymizer_session()


async def close_all_sessions():
    """Close all instantiated sessions"""
    await get_ublox_api_session().aclose()
    await get_accounting_session().aclose()
    await get_anonymizer_session().aclose()
