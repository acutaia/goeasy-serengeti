#!/usr/bin/env python3
"""
IPT-Anonymizer mocked Http requests

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2021 Angelo Cutaia

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
from asyncio import TimeoutError

# Third Party
from aiohttp import ClientError
from aioresponses import aioresponses
from fastapi import status
import orjson

# Internal
from .constants import MOCKED_RESPONSE

# ----------------------------------------------------------------------------------------------


def correct_store_in_ipt_anonymizer(m: aioresponses, url: str):
    m.post(
        url=url, status=status.HTTP_200_OK, body=orjson.dumps(MOCKED_RESPONSE).decode()
    )


def unreachable_store_in_ipt_anonymizer(m: aioresponses, url: str):
    m.post(url=url, exception=ClientError("Host unreachable"))


def starvation_store_in_ipt_anonymizer(m: aioresponses, url: str):
    m.post(url=url, exception=TimeoutError("Starvation"))


# ----------------------------------------------------------------------------------------------
