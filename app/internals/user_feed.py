#!/usr/bin/env python3
"""
UserFeed utilities package

:author: Angelo Cutaia
:copyright: Copyright 2020, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

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
import asyncio
from datetime import datetime
import sys

# Third Party
from aiologger.loggers.json import JsonLogger
import httpx
import orjson

# Internal
from .position_alteration_detection import haversine
from .ublox_api import get_galileo_message, get_ublox_token, get_galileo_message_list
from .anonymizer import store_user_in_the_anonengine
from .accounting_manager import store_in_iota
from ..models.user_feed.user import UserFeedInput
from ..models.security import Authenticity
from ..config import get_ublox_api_settings

logger = JsonLogger.with_default_handlers(
    name="user-feed",
    serializer_kwargs={"indent": 4}
)

# --------------------------------------------------------------------------------------------


async def end_to_end_position_authentication(
        user_feed: UserFeedInput,
        timestamp: datetime,
        host: str,
        journey_id: str = "TEST",
        source_app: str = "TEST",
        client_id: str = "TEST",
        user_id: str = "TEST"
) -> UserFeedInput:
    """
    Contact Ublox-API and validate Android Data

    :param user_feed: data to validate
    :param timestamp: when the request was received
    :param host: who made the request
    :param journey_id: uuid4 associated to the request ("TEST" only for testing purposes)
    :param source_app: app that made the request ("TEST" only for testing purposes)
    :param client_id: client_id expressed by the token ("TEST" only for testing purposes)
    :param user_id: user_id expressed by the token ("TEST" only for testing purposes)
    :return: data validated
    """

    # Initialize
    galileo_auth_number = 0
    authentic_number = 0
    not_authentic_number = 0
    unknown_number = 0

    # Get Ublox-APi token and settings
    ublox_api_settings = get_ublox_api_settings()
    ublox_token = await get_ublox_token(ublox_api_settings)

    # Contact Ublox-Api for every position
    async with httpx.AsyncClient(verify=False) as client:

        for position in user_feed.trace_information:
            # Find the location of the position (Sweden or Italy)
            location = haversine(position.lat, position.lon)

            for auth in position.galileo_auth:

                galileo_auth_number += 1
                galileo_data = await get_galileo_message(
                    client,
                    auth.svid,
                    auth.time,
                    ublox_token,
                    ublox_api_settings,
                    location
                )

                if galileo_data is None:
                    position.authenticity = Authenticity.unknown
                    unknown_number += 1
                    break

                elif galileo_data == auth.data:
                    position.authenticity = Authenticity.authentic
                    authentic_number += 1

                else:
                    position.authenticity = Authenticity.not_authentic
                    not_authentic_number += 1
                    # Remake the request
                    galileo_data_list = await get_galileo_message_list(
                        client,
                        auth.svid,
                        auth.time,
                        ublox_token,
                        ublox_api_settings,
                        location
                    )
                    for data in galileo_data_list:
                        if data.raw_data == auth.data:
                            position.authenticity = Authenticity.authentic
                            authentic_number += 1
                            not_authentic_number -= 1
                            break
                    if position.authenticity == Authenticity.not_authentic:
                        logger.warning(
                            {
                                "message_timestamp": auth.time,
                                "android_message": auth.data,
                                "satellite_id": auth.svid,
                                "status": "Real Fake",
                                "ublox_api_messages": [
                                    ublox_api.dict()
                                    for ublox_api in galileo_data_list
                                ]
                            }
                        )

    logger.debug(
        {
            "host": host,
            "source_app": source_app,
            "journey_id": journey_id,
            "galileo_auth": galileo_auth_number,
            "authentic": authentic_number,
            "not_authentic": not_authentic_number,
            "unknown": unknown_number,
            "analysis_time": f"{datetime.now() - timestamp}"
        }
    )
    asyncio.create_task(
        store_in_iota(
            source_app=source_app,
            client_id=client_id,
            user_id=user_id,
            msg_id=journey_id,
            msg_size=sys.getsizeof(user_feed.json()),
            msg_time=timestamp,
            msg_malicious_position=not_authentic_number,
            msg_authenticated_position=authentic_number,
            msg_unknown_position=unknown_number,
            msg_total_position=galileo_auth_number,

        )
    )

    return user_feed


async def store_android_data(
        user_feed_input: UserFeedInput,
        timestamp: datetime,
        host: str,
        journey_id: str,
        source_app: str,
        client_id: str,
        user_id: str
) -> None:
    """
    Store UserFeed data in the anonymizer in a correct format

    :param user_feed_input: data to validate
    :param timestamp: when the request was received
    :param host: who made the request
    :param journey_id: uuid4 associated to the request
    :param source_app: app that made the request
    :param client_id: client_id expressed by the token
    :param user_id: user_id expressed by the token
    """
    try:
        user_feed = await end_to_end_position_authentication(
            user_feed=user_feed_input,
            timestamp=timestamp,
            host=host,
            journey_id=journey_id,
            source_app=source_app,
            client_id=client_id,
            user_id=user_id
        )

        user_feed_output =orjson.dumps(
            {
                "behaviour": {
                    "app_defined_behaviour": user_feed.behaviour.app_defined,
                    "tpv_defined_behaviour": user_feed.behaviour.tpv_defined,
                    "user_defined_behaviour": user_feed.behaviour.user_defined
                },
                "company_code": user_feed.company_code,
                "company_trip_type": user_feed.company_trip_type.value,
                "deviceId": user_feed.id,
                "journeyId": journey_id,
                "startDate": user_feed.startDate,
                "endDate": user_feed.endDate,
                "distance": user_feed.distance,
                "elapsedTime": user_feed.elapsedTime,
                "positions": [
                    {
                        "authenticity": position.authenticity,
                        "lat": position.lat,
                        "lon": position.lon,
                        "time": position.time,
                        "partialDistance": position.partialDistance
                    }
                    for position in user_feed.trace_information
                ],
                "sensors": user_feed.sensors_information,
                "mainTypeSpace": user_feed.mainTypeSpace,
                "mainTypeTime": user_feed.mainTypeTime,
                "source_app": source_app
                }
        )
        await store_user_in_the_anonengine(user_feed_output)
    finally:
        return