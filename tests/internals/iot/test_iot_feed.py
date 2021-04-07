#!/usr/bin/env python3
"""
Tests app.internals.iot module

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
import time

# Test
from aioresponses import aioresponses
from fastapi import HTTPException
import respx
import pytest
import uvloop

# Internal
from app.internals.iot import end_to_end_position_authentication, store_iot_data
from app.internals.keycloak import KEYCLOACK
from app.models.iot_feed.iot import IotInput

from app.models.security import Authenticity

from tests.mock.ublox_api.get_raw_data import (
    correct_get_raw_data,
    unreachable_get_raw_data
)
from tests.mock.ublox_api.get_ublox_api_list import (
    correct_get_ublox_api_list,
    unreachable_get_ublox_api_list
)

from tests.mock.anonymizer.anonengine import correct_store_iot_in_the_anonengine
from tests.mock.keycloack.keycloack import correct_get_blox_token
from tests.mock.ublox_api.constants import (
    RaW_Ublox,
    URL_GET_UBLOX,
    URL_POST_UBLOX
)

from tests.mock.accounting_manager.iota import correct_store_in_iota
from .constants import IOT_INPUT_PATH
from ..logger import disable_logger

# ---------------------------------------------------------------------------------------------

with open(IOT_INPUT_PATH, "r") as fp:
    IOT_INPUT = IotInput.parse_raw(fp.read())
    """IotInput Data"""

# ---------------------------------------------------------------------------------------------


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


class TestIotFeed:
    """
    Test the iot module
    """
    @respx.mock
    @pytest.mark.asyncio
    async def test_end_to_end_position_authentication(self, mock_aioresponse):
        """ Test the behaviour of end_to_end_position_authentication """

        # Disable the logger of the app
        disable_logger()

        # Setup Keycloack and mock the request
        correct_get_blox_token(mock_aioresponse)
        # during the setup we'll obtain a token that will be stored in cls.last_token
        await KEYCLOACK.setup()

        # Position authentic
        correct_get_raw_data(url=URL_GET_UBLOX, raw_data=RaW_Ublox)
        correct_store_in_iota()

        iot_output = await end_to_end_position_authentication(
            iot_input=IOT_INPUT,
            timestamp=time.time(),
            host="localhost",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST",
            obesrvation_gepid="TEST"
        )

        # Check if the object was generated well
        assert iot_output["result"]["authenticity"] == Authenticity.authentic, "The position is authentic"

        # Position Unknown
        correct_get_raw_data(url=URL_GET_UBLOX, raw_data=None)

        iot_output = await end_to_end_position_authentication(
            iot_input=IOT_INPUT,
            timestamp=time.time(),
            host="localhost",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST",
            obesrvation_gepid="TEST"
        )

        # Check if the object was generated well
        assert iot_output["result"]["authenticity"] == Authenticity.unknown, "The position is unknown"

        # Position false fake
        correct_get_raw_data(url=URL_GET_UBLOX, raw_data="FALSE_FAKE")
        correct_get_ublox_api_list(url=URL_POST_UBLOX, raw_data=RaW_Ublox)

        iot_output = await end_to_end_position_authentication(
            iot_input=IOT_INPUT,
            timestamp=time.time(),
            host="localhost",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST",
            obesrvation_gepid="TEST"
        )

        # Check if the object was generated well
        assert iot_output["result"]["authenticity"] == Authenticity.authentic, "The position is authentic"

        # Position real fake
        correct_get_raw_data(url=URL_GET_UBLOX, raw_data="FAKE")
        correct_get_ublox_api_list(url=URL_POST_UBLOX, raw_data="REAL_FAKE")

        iot_output = await end_to_end_position_authentication(
            iot_input=IOT_INPUT,
            timestamp=time.time(),
            host="localhost",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST",
            obesrvation_gepid="TEST"
        )

        # Check if the object was generated well
        assert iot_output["result"]["authenticity"] == Authenticity.not_authentic, "The position is not authentic"

        # Something went wrong during the request of a single raw_data
        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_raw_data(url=URL_GET_UBLOX)
            await end_to_end_position_authentication(
                iot_input=IOT_INPUT,
                timestamp=time.time(),
                host="localhost",
                source_app="TEST",
                client_id="TEST",
                user_id="TEST",
                obesrvation_gepid="TEST"
            )

        # Something went wrong during the request of a List[UbloxApi]
        with pytest.raises(HTTPException):
            # Mock the requests
            correct_get_raw_data(url=URL_GET_UBLOX, raw_data="FALSE_FAKE")
            unreachable_get_ublox_api_list(url=URL_POST_UBLOX)
            await end_to_end_position_authentication(
                iot_input=IOT_INPUT,
                timestamp=time.time(),
                host="localhost",
                source_app="TEST",
                client_id="TEST",
                user_id="TEST",
                obesrvation_gepid="TEST"
            )

    @respx.mock
    @pytest.mark.asyncio
    async def test_store_iot_data(self, mock_aioresponse):
        """ Test the behaviour of store_iot_data """

        # Disable the logger of the app
        disable_logger()

        # Setup Keycloack and mock the request
        correct_get_blox_token(mock_aioresponse)
        # during the setup we'll obtain a token that will be stored in cls.last_token
        await KEYCLOACK.setup()

        # Mock the other requests
        correct_get_raw_data(url=URL_GET_UBLOX, raw_data=RaW_Ublox)
        correct_store_in_iota()
        correct_store_iot_in_the_anonengine()

        # Check if everything went ok
        await store_iot_data(
            iot_input=IOT_INPUT,
            timestamp=time.time(),
            host="localhost",
            obesrvation_gepid="TEST",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST"
        )
