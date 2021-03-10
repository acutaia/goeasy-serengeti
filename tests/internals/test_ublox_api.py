#!/usr/bin/env python3
"""
Tests app.internal.ublox_api module

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
import httpx

# Test
from fastapi import HTTPException
import respx
import pytest
import uvloop

# Internal
from app.internals.ublox_api import (
    get_ublox_token,
    get_galileo_message,
    get_ublox_message,
    get_galileo_messages_list,
    get_ublox_messages_list,
    construct_request
)

from .logger import disable_logger
from ..mock.ublox_api.constants import (
    FAKE_TOKEN_FOR_TESTING,
    URL_GET_UBLOX,
    URL_GET_GALILEO,
    URL_POST_UBLOX,
    URL_POST_GALILEO,
    RaW_Galileo,
    RaW_Ublox,
    SvID,
    TIMESTAMP,
    LOCATION,
    NUMBER_REQUESTED_DATA
)
from ..mock.ublox_api.get_token import (
    correct_get_blox_token,
    unreachable_get_ublox_token,
    unauthorized_get_ublox_token
)
from ..mock.ublox_api.get_raw_data import (
    correct_get_raw_data,
    ublox_api_unreachable_get_raw_data,
    token_expired_get_raw_data
)
from ..mock.ublox_api.get_ublox_api_list import (
    correct_get_ublox_api_list,
    ublox_api_unreachable_get_ublox_api_list,
    token_expired_get_ublox_api_list
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


class TestUbloxApi:
    """
     Test the ublox_api module
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_ublox_token(self):
        """ Test the behaviour of get_ublox_token """

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_get_blox_token()
        token = await get_ublox_token()
        assert FAKE_TOKEN_FOR_TESTING == token, "Token must be the same"

        # Check if raises an exception in case of unauthorized user
        with pytest.raises(HTTPException):
            # Mock the request
            unauthorized_get_ublox_token()
            await get_ublox_token()

        # Check if raises an exception in case of unreachable host
        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_ublox_token()
            await get_ublox_token()

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_galileo_message(self):
        """ Test the behaviour of get_galileo_message """

        # Disable the logger of the app
        disable_logger()

        async with httpx.AsyncClient() as client:
            # Mock the request
            correct_get_raw_data(url=URL_GET_GALILEO, raw_data=RaW_Galileo)
            raw_data = await get_galileo_message(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                location=LOCATION,
                ublox_token=FAKE_TOKEN_FOR_TESTING
            )
            assert raw_data == RaW_Galileo, "Raw Galileo data must be the same"

            # Mock the request
            token_expired_get_raw_data(url=URL_GET_GALILEO, raw_data=RaW_Galileo)
            raw_data = await get_galileo_message(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                location=LOCATION,
                ublox_token=FAKE_TOKEN_FOR_TESTING
            )
            assert raw_data == RaW_Galileo, "Raw Galileo data must be the same"

            # Mock the request
            ublox_api_unreachable_get_raw_data(URL_GET_GALILEO)
            # Check if raises an exception in case of unreachable host
            with pytest.raises(HTTPException):
                await get_galileo_message(
                    client=client,
                    svid=SvID,
                    timestamp=TIMESTAMP,
                    location=LOCATION,
                    ublox_token=FAKE_TOKEN_FOR_TESTING
                )

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_ublox_message(self):
        """ Test the behaviour of get_ublox_message """

        # Disable the logger of the app
        disable_logger()

        async with httpx.AsyncClient() as client:
            # Mock the request
            correct_get_raw_data(url=URL_GET_UBLOX, raw_data=RaW_Ublox)
            raw_data = await get_ublox_message(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                location=LOCATION,
                ublox_token=FAKE_TOKEN_FOR_TESTING
            )
            assert raw_data == RaW_Ublox, "Raw Ublox data must be the same"

            # Mock the request
            token_expired_get_raw_data(url=URL_GET_UBLOX, raw_data=RaW_Ublox)
            raw_data = await get_ublox_message(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                location=LOCATION,
                ublox_token=FAKE_TOKEN_FOR_TESTING
            )
            assert raw_data == RaW_Ublox, "Raw Ublox data must be the same"

            # Mock the request
            ublox_api_unreachable_get_raw_data(URL_GET_UBLOX)
            # Check if raises an exception in case of unreachable host
            with pytest.raises(HTTPException):
                await get_ublox_message(
                    client=client,
                    svid=SvID,
                    timestamp=TIMESTAMP,
                    location=LOCATION,
                    ublox_token=FAKE_TOKEN_FOR_TESTING
                )

    def test_construct_request(self):
        """ Test the construction of the body of the request made to Ublox-Api """
        request = construct_request(svid=SvID, timestamp=TIMESTAMP)

        assert len(request["info"]) == NUMBER_REQUESTED_DATA, "Incorrect number of data requested"

        for ublox_api in request["info"]:
            assert ublox_api["raw_data"] is None, "Incorrect format of the request"
            assert (
                    TIMESTAMP != ublox_api["timestamp"] and
                    (
                            TIMESTAMP - 1000 * NUMBER_REQUESTED_DATA
                    ) <= ublox_api["timestamp"] <= (
                            TIMESTAMP + 1000 * NUMBER_REQUESTED_DATA
                    )
            ), "Incorrect format of the request"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_galileo_messages_list(self):
        """ Test the behaviour of get_galileo_messages_list """

        # Disable the logger of the app
        disable_logger()

        async with httpx.AsyncClient() as client:
            # Mock the request
            correct_get_ublox_api_list(url=URL_POST_GALILEO, raw_data=RaW_Galileo)
            ublox_api_list = await get_galileo_messages_list(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                ublox_token=FAKE_TOKEN_FOR_TESTING,
                location=LOCATION
            )
            assert [
                {
                    "timestamp": TIMESTAMP,
                    "raw_data": RaW_Galileo
                }
            ] == ublox_api_list, "List of UbloxApi data must be the same"

            # Mock the request
            token_expired_get_ublox_api_list(url=URL_POST_GALILEO, raw_data=RaW_Galileo)
            ublox_api_list = await get_galileo_messages_list(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                ublox_token=FAKE_TOKEN_FOR_TESTING,
                location=LOCATION
            )

            assert [
                {
                    "timestamp": TIMESTAMP,
                    "raw_data": RaW_Galileo
                }
            ] == ublox_api_list, "List of UbloxApi data must be the same"

            # Mock the request
            ublox_api_unreachable_get_ublox_api_list(url=URL_POST_GALILEO)
            with pytest.raises(HTTPException):
                await get_galileo_messages_list(
                    client=client,
                    svid=SvID,
                    timestamp=TIMESTAMP,
                    ublox_token=FAKE_TOKEN_FOR_TESTING,
                    location=LOCATION
                )

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_ublox_messages_list(self):
        """ Test the behaviour of get_ublox_messages_list """

        # Disable the logger of the app
        disable_logger()

        async with httpx.AsyncClient() as client:
            # Mock the request
            correct_get_ublox_api_list(url=URL_POST_UBLOX, raw_data=RaW_Ublox)
            ublox_api_list = await get_ublox_messages_list(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                ublox_token=FAKE_TOKEN_FOR_TESTING,
                location=LOCATION
            )
            assert [
                       {
                           "timestamp": TIMESTAMP,
                           "raw_data": RaW_Ublox
                       }
                   ] == ublox_api_list, "List of UbloxApi data must be the same"

            # Mock the request
            token_expired_get_ublox_api_list(url=URL_POST_UBLOX, raw_data=RaW_Ublox)
            ublox_api_list = await get_ublox_messages_list(
                client=client,
                svid=SvID,
                timestamp=TIMESTAMP,
                ublox_token=FAKE_TOKEN_FOR_TESTING,
                location=LOCATION
            )

            assert [
                       {
                           "timestamp": TIMESTAMP,
                           "raw_data": RaW_Ublox
                       }
                   ] == ublox_api_list, "List of UbloxApi data must be the same"

            # Mock the request
            ublox_api_unreachable_get_ublox_api_list(url=URL_POST_UBLOX)
            with pytest.raises(HTTPException):
                await get_ublox_messages_list(
                    client=client,
                    svid=SvID,
                    timestamp=TIMESTAMP,
                    ublox_token=FAKE_TOKEN_FOR_TESTING,
                    location=LOCATION
                )