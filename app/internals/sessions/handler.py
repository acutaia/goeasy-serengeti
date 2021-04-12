#!/usr/bin/env python3
"""
Sessions handler

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
import asyncio

# Internal
from .accounting_manager import get_accounting_session
from .anonymizer import get_anonengine_session
from .ipt_anonymizer import get_ipt_anonymizer_session
from .ublox_api import get_ublox_api_session
from ..keycloak import KEYCLOACK

# ----------------------------------------------------------------------------


async def instantiate_all_sessions():
    """instantiate all sessions included in serengeti"""
    get_accounting_session()
    get_anonengine_session()
    get_ipt_anonymizer_session()
    get_ublox_api_session()
    await KEYCLOACK.setup()


async def close_all_sessions():
    """Close all instantiated sessions"""
    ublox = asyncio.create_task(get_ublox_api_session().close())
    iota = asyncio.create_task(get_accounting_session().close())
    anonymizer = asyncio.create_task(get_anonengine_session().close())
    ipt_anonymizer = asyncio.create_task(get_accounting_session().close())
    keycloack = asyncio.create_task(KEYCLOACK.close())
    await asyncio.gather(
        *[ublox, iota, anonymizer, ipt_anonymizer, keycloack], return_exceptions=True
    )