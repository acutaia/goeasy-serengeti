#!/usr/bin/env python3
"""
Tests app.internals.ipt_anonymizer module

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
from app.internals.ipt_anonymizer import store_in_the_anonymizer
from .logger import disable_logger
from ..mock.anonymizer.constants import URL_STORE_USER_DATA, URL_STORE_IOT_DATA
from ..mock.anonymizer.ipt import (
    correct_store_in_ipt_anonymizer,
    unreachable_store_in_ipt_anonymizer,
    starvation_store_in_ipt_anonymizer,
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


class TestIPTAnonymizer:
    """
    Test the ipt_anonymizer module
    """

    @pytest.mark.asyncio
    async def test_store_in_the_anonymizer(self, mock_aioresponse):
        """ Test the behaviour of store_user_in_the_anonengine """

        # Disable the logger of the app
        disable_logger()

        for url in (URL_STORE_USER_DATA, URL_STORE_IOT_DATA):
            # Mock the request
            correct_store_in_ipt_anonymizer(mock_aioresponse, url)
            assert (
                await store_in_the_anonymizer({"Foo": "Bar"}, url) is None
            ), "We aren't interested in the response"

            with pytest.raises(HTTPException):
                # Mock the request
                unreachable_store_in_ipt_anonymizer(mock_aioresponse, url)
                await store_in_the_anonymizer({"Foo": "Bar"}, URL_STORE_USER_DATA)

            with pytest.raises(HTTPException):
                # Mock the request
                starvation_store_in_ipt_anonymizer(mock_aioresponse, url)
                await store_in_the_anonymizer({"Foo": "Bar"}, URL_STORE_USER_DATA)
