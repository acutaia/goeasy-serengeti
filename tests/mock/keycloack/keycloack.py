"""
Mocked keycloack http requests

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

# Third Party
from aiohttp import ServerTimeoutError
from aioresponses import aioresponses
from fastapi import status
import orjson

# Internal
from .constants import FAKE_TOKEN_FOR_TESTING, TOKEN_REQUEST_URL

# ----------------------------------------------------------------------------------------------


def correct_get_blox_token(m: aioresponses):
    """Mock the request made to keycloack to obtain a valid token"""
    m.post(
        TOKEN_REQUEST_URL,
        status=status.HTTP_200_OK,
        body=orjson.dumps(
            {
                "access_token": FAKE_TOKEN_FOR_TESTING
            }
        ).decode()
    )


def new_correct_get_blox_token(m: aioresponses):
    """Mock the request made to keycloack to obtain a valid token"""
    m.post(
        TOKEN_REQUEST_URL,
        status=status.HTTP_200_OK,
        body=orjson.dumps(
            {
                "access_token": "NEW_TOKEN"
            }
        ).decode()
    )


def unauthorized_get_ublox_token(m: aioresponses):
    """Mock the request made to keycloack to obtain a valid token"""

    m.post(
        TOKEN_REQUEST_URL,
        status=status.HTTP_401_UNAUTHORIZED
    )


def unreachable_get_ublox_token(m: aioresponses):
    """Mock the request made to keycloack to obtain a valid token"""
    m.post(
        TOKEN_REQUEST_URL,
        exception=ServerTimeoutError("Timeout")
    )


