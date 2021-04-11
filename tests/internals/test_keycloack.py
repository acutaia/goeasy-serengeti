#!/usr/bin/env python3
"""
Tests app.internals.keycloack module

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

# Test
from aioresponses import aioresponses
from fastapi import HTTPException
import pytest
import uvloop

# Internal
from app.internals.keycloak import KEYCLOACK
from .logger import disable_logger
from ..mock.keycloack.keycloack import (
    correct_get_blox_token,
    new_correct_get_blox_token,
    unreachable_get_ublox_token,
    unauthorized_get_ublox_token,
)

# ------------------------------------------------------------------------------


@pytest.fixture()
def event_loop():
    """
    Set uvloop as the default event loop
    """
    loop = uvloop.Loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


class TestKeycloack:
    """
     Test the ublox_api module
    """

    @pytest.mark.asyncio
    async def test_get_token(self, mock_aioresponse):
        """ Test the behaviour of get_ublox_token """

        # Disable the logger of the app
        disable_logger()

        # Setup Keycloack and mock the request
        correct_get_blox_token(mock_aioresponse)
        # during the setup we'll obtain a token that will be stored in cls.last_token
        await KEYCLOACK.setup()

        # Check if we used the cached token
        assert await KEYCLOACK.get_ublox_token() == KEYCLOACK.last_token, "Token must be the same"

        # clean the cache
        KEYCLOACK.last_token_reception_time = 0
        last_token = KEYCLOACK.last_token

        # Mock the request
        new_correct_get_blox_token(mock_aioresponse)
        assert await KEYCLOACK.get_ublox_token() != last_token, "Token must be different"

        # clean the cache
        KEYCLOACK.last_token_reception_time = 0

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_ublox_token(mock_aioresponse)
            await KEYCLOACK.get_ublox_token()

        with pytest.raises(HTTPException):
            # Mock the request
            unauthorized_get_ublox_token(mock_aioresponse)
            await KEYCLOACK.get_ublox_token()

        await KEYCLOACK.close()
