"""
Tests app.internals.accounting_manager module

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
from datetime import datetime
import time

# Test
from aioresponses import aioresponses
from fastapi import HTTPException
import pytest
import uvloop

# Internal
from app.internals.accounting_manager import get_iota_user, store_in_iota
from .logger import disable_logger
from ..mock.accounting_manager.iota import (
    correct_get_iota_user,
    correct_store_in_iota,
    unreachable_get_iota_user,
    unreachable_store_in_iota,
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


class TestAccountingManager:
    """
    Test the accounting_manager module
    """

    @pytest.mark.asyncio
    async def test_get_iota_user(self, mock_aioresponse):
        """Test the behaviour of get_iota_user"""

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_get_iota_user(mock_aioresponse, user="TEST")
        assert await get_iota_user(user=f"TEST-{datetime.now().date()}") == {
            "user": "TEST"
        }, "User must be the same"

        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_iota_user(mock_aioresponse, user="TEST")
            await get_iota_user(user=f"TEST-{datetime.now().date()}")

    @pytest.mark.asyncio
    async def test_store_iota_user(self, mock_aioresponse):
        """Test the behaviour of store_iota_user"""

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_store_in_iota(mock_aioresponse)
        assert (
            await store_in_iota(
                source_app="TEST",
                client_id="TEST",
                user_id="TEST",
                msg_id="TEST",
                msg_size=0,
                msg_time=time.time(),
                msg_total_position=0,
                msg_authenticated_position=0,
                msg_unknown_position=0,
                msg_malicious_position=0,
            )
            is None
        ), "We aren't interested in the response"

        # Mock the request
        unreachable_store_in_iota(mock_aioresponse)
        # The exceptions in store in iota are ignored, they are only logged
        assert (
            await store_in_iota(
                source_app="TEST",
                client_id="TEST",
                user_id="TEST",
                msg_id="TEST",
                msg_size=0,
                msg_time=time.time(),
                msg_total_position=0,
                msg_authenticated_position=0,
                msg_unknown_position=0,
                msg_malicious_position=0,
            )
            is None
        ), "We aren't interested in the response"
