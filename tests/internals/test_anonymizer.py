#!/usr/bin/env python3
"""
Tests app.internals.anonymizer module

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
from fastapi import HTTPException
import respx
import pytest
import uvloop

# Internal
from app.internals.anonymizer import store_user_in_the_anonengine, extract_details, extract_mobility
from .logger import disable_logger
from ..mock.anonymizer.constants import MOCKED_RESPONSE
from ..mock.anonymizer.anonengine import (
    correct_store_user_in_the_anonengine,
    unreachable_store_user_in_the_anonengine,
    correct_extract_details,
    unreachable_extract_details,
    correct_extract_mobility,
    unreachable_extract_mobility
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


class TestAnonengine:
    """
    Test the anonymizer module
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_store_user_in_the_anonengine(self):
        """ Test the behaviour of store_user_in_the_anonengine """

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_store_user_in_the_anonengine()
        assert await store_user_in_the_anonengine({"Foo": "Bar"}) is None, "We aren't interested in the response"

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_store_user_in_the_anonengine()
            await store_user_in_the_anonengine({"Foo": "Bar"})

    @respx.mock
    @pytest.mark.asyncio
    async def test_extract_details(self):
        """ Test the behaviour of correct_extract_details """

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_extract_details(journey_id="TEST")
        assert await extract_details(journey_id="TEST") == MOCKED_RESPONSE, "Response must be the same"

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_extract_details(journey_id="TEST")
            await extract_details(journey_id="TEST")

    @respx.mock
    @pytest.mark.asyncio
    async def test_extract_mobility(self):
        """ Test the behaviour of correct_extract_details """

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_extract_mobility(journey_id="TEST")
        assert await extract_mobility(journey_id="TEST") == MOCKED_RESPONSE, "Response must be the same"

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_extract_mobility(journey_id="TEST")
            await extract_mobility(journey_id="TEST")


