"""
Tests app.internals.keycloak module

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

# Test
from aioresponses import aioresponses
from fastapi import HTTPException
import pytest
import uvloop

# Internal
from app.internals.keycloak import KEYCLOAK
from .logger import disable_logger
from ..mock.keycloak.keycloak import (
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


class TestKEYCLOAK:
    """
    Test the ublox_api module
    """

    @pytest.mark.asyncio
    async def test_get_token(self, mock_aioresponse):
        """Test the behaviour of get_ublox_token"""

        # Disable the logger of the app
        disable_logger()

        # Setup KEYCLOAK and mock the request
        correct_get_blox_token(mock_aioresponse)
        # during the setup we'll obtain a token that will be stored in cls.last_token
        await KEYCLOAK.setup()

        # Check if we used the cached token
        assert (
            await KEYCLOAK.get_ublox_token() == KEYCLOAK.last_token
        ), "Token must be the same"

        # clean the cache
        KEYCLOAK.last_token_reception_time = 0
        last_token = KEYCLOAK.last_token

        # Mock the request
        new_correct_get_blox_token(mock_aioresponse)
        assert await KEYCLOAK.get_ublox_token() != last_token, "Token must be different"

        # clean the cache
        KEYCLOAK.last_token_reception_time = 0

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_ublox_token(mock_aioresponse)
            await KEYCLOAK.get_ublox_token()

        with pytest.raises(HTTPException):
            # Mock the request
            unauthorized_get_ublox_token(mock_aioresponse)
            await KEYCLOAK.get_ublox_token()

        await KEYCLOAK.close()
