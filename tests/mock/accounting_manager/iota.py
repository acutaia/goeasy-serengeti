"""
Mocked IoTa requests

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0

..

    Copyright 2021 LINKS Foundation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
from asyncio import TimeoutError
from datetime import datetime

# Third Party
from aioresponses import aioresponses
from fastapi import status
import orjson

# Internal
from .constants import URL_GET_IOTA_USER, URL_STORE_IN_IOTA

# -------------------------------------------------------------------------------


def correct_get_iota_user(m: aioresponses, user: str):
    """Mocked get iota user"""
    m.get(
        f"{URL_GET_IOTA_USER}?user={user}-{datetime.now().date()}",
        status=status.HTTP_200_OK,
        body=orjson.dumps({"user": user}).decode(),
    )


def unreachable_get_iota_user(m: aioresponses, user: str):
    """Mocked get iota user"""
    m.get(
        f"{URL_GET_IOTA_USER}?user={user}-{datetime.now().date()}",
        exception=TimeoutError("Timeout"),
    )


# -------------------------------------------------------------------------------


def correct_store_in_iota(m: aioresponses):
    """Mocked store in iota"""
    m.post(URL_STORE_IN_IOTA, status=status.HTTP_200_OK)


def unreachable_store_in_iota(m: aioresponses):
    """Mocked store in iota"""
    m.post(URL_STORE_IN_IOTA, exception=TimeoutError("Timeout"))
