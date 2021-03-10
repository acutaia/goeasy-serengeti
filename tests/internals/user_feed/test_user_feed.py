#!/usr/bin/env python3
"""
Tests app.internals.user_feed module

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
import os
import time

# Test
from fastapi import HTTPException
import respx
import pytest
import uvloop

# Internal
from app.internals.user_feed import (
    end_to_end_position_authentication,
    store_android_data
)
from app.models.user_feed.user import (
    UserFeedInput,
    UserFeedOutput,
    PositionObject
)

from app.models.security import Authenticity

from tests.mock.ublox_api.get_raw_data import (
    correct_get_raw_data,
    unreachable_get_raw_data
)
from tests.mock.ublox_api.get_ublox_api_list import (
    correct_get_ublox_api_list,
    unreachable_get_ublox_api_list
)

from tests.mock.ublox_api.get_token import correct_get_blox_token

from tests.mock.ublox_api.constants import (
    RaW_Galileo,
    URL_GET_GALILEO,
    URL_POST_GALILEO
)

from tests.mock.accounting_manager.iota import correct_store_in_iota
from tests.mock.anonymizer.anonengine import correct_store_user_in_the_anonengine
from ..logger import disable_logger

# ---------------------------------------------------------------------------------------------

with open(
        os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)
            ), "fake_user_feed.json"
        ),
        "r"
) as fp:
    USER_INPUT = UserFeedInput.parse_raw(fp.read())
    """UserFeedInput Data"""

# ---------------------------------------------------------------------------------------------


@pytest.fixture()
def event_loop():
    """
    Set uvloop as the default event loop
    """
    loop = uvloop.Loop()
    yield loop
    loop.close()


class TestUserFeed:
    """
    Test the user_feed module
    """
    @respx.mock
    @pytest.mark.asyncio
    async def test_end_to_end_position_authentication(self):
        """ Test the behaviour of end_to_end_position_authentication """

        # Disable the logger of the app
        disable_logger()

        # Mock the request
        correct_get_blox_token()

        # Position authentic
        correct_get_raw_data(url=URL_GET_GALILEO, raw_data=RaW_Galileo)
        correct_store_in_iota()

        user_feed_validated = await end_to_end_position_authentication(
            user_feed=USER_INPUT,
            timestamp=time.time(),
            host="localhost"
        )
        assert user_feed_validated.trace_information[0].authenticity == Authenticity.authentic, "The position is authentic"

        # Position Unknown
        correct_get_raw_data(url=URL_GET_GALILEO, raw_data=None)

        user_feed_validated = await end_to_end_position_authentication(
            user_feed=USER_INPUT,
            timestamp=time.time(),
            host="localhost"
        )
        assert user_feed_validated.trace_information[0].authenticity == Authenticity.unknown, "The position is unknown"

        # Position false fake
        correct_get_raw_data(url=URL_GET_GALILEO, raw_data="FALSE_FAKE")
        correct_get_ublox_api_list(url=URL_POST_GALILEO, raw_data=RaW_Galileo)

        user_feed_validated = await end_to_end_position_authentication(
            user_feed=USER_INPUT,
            timestamp=time.time(),
            host="localhost"
        )
        assert user_feed_validated.trace_information[0].authenticity == Authenticity.authentic, "The position is authentic"

        # Position real fake
        correct_get_raw_data(url=URL_GET_GALILEO, raw_data="FAKE")
        correct_get_ublox_api_list(url=URL_POST_GALILEO, raw_data="REAL_FAKE")

        user_feed_validated = await end_to_end_position_authentication(
            user_feed=USER_INPUT,
            timestamp=time.time(),
            host="localhost"
        )
        assert user_feed_validated.trace_information[0].authenticity == Authenticity.not_authentic, "The position is not authentic"

        # Something went wrong during the request of a single raw_data
        with pytest.raises(HTTPException):
            # Mock the request
            unreachable_get_raw_data(url=URL_GET_GALILEO)
            await end_to_end_position_authentication(
                user_feed=USER_INPUT,
                timestamp=time.time(),
                host="localhost"
            )

        # Something went wrong during the request of a List[UbloxApi]
        with pytest.raises(HTTPException):
            # Mock the requests
            correct_get_raw_data(url=URL_GET_GALILEO, raw_data="FALSE_FAKE")
            unreachable_get_ublox_api_list(url=URL_POST_GALILEO)
            await end_to_end_position_authentication(
                user_feed=USER_INPUT,
                timestamp=time.time(),
                host="localhost"
            )

    @respx.mock
    @pytest.mark.asyncio
    async def test_store_android_data(self):
        """ Test the behaviour of store_android_data """

        # Disable the logger of the app
        disable_logger()

        # Mock the requests
        correct_get_blox_token()
        correct_get_raw_data(url=URL_GET_GALILEO, raw_data=RaW_Galileo)
        correct_store_in_iota()
        correct_store_user_in_the_anonengine()

        user_feed_validated = await end_to_end_position_authentication(
            user_feed=USER_INPUT,
            timestamp=time.time(),
            host="localhost"
        )

        # Check if the conversion in user_feed_output is correct
        user_feed_output = {
                "app_defined_behaviour": user_feed_validated.behaviour.app_defined,
                "tpv_defined_behaviour": user_feed_validated.behaviour.tpv_defined,
                "user_defined_behaviour": user_feed_validated.behaviour.user_defined,
                "company_code": user_feed_validated.company_code,
                "company_trip_type": user_feed_validated.company_trip_type,
                "deviceId": user_feed_validated.id,
                "journeyId": "TEST",
                "startDate": user_feed_validated.startDate,
                "endDate": user_feed_validated.endDate,
                "distance": user_feed_validated.distance,
                "elapsedTime": user_feed_validated.elapsedTime,
                "positions": [
                    PositionObject.parse_obj(
                        {
                            "authenticity": position.authenticity,
                            "lat": position.lat,
                            "lon": position.lon,
                            "partialDistance": position.partialDistance,
                            "time": position.time
                        }
                    )
                    for position in user_feed_validated.trace_information
                ],
                "sensors": user_feed_validated.sensors_information,
                "mainTypeSpace": user_feed_validated.mainTypeSpace,
                "mainTypeTime": user_feed_validated.mainTypeTime,
                "sourceApp": "TEST"
            }

        UserFeedOutput.parse_obj(user_feed_output)

        # Check if everything went ok
        await store_android_data(
            user_feed_input=USER_INPUT,
            timestamp=time.time(),
            host="localhost",
            journey_id="TEST",
            source_app="TEST",
            client_id="TEST",
            user_id="TEST"
        )



