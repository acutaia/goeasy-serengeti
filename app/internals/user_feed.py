#!/usr/bin/env python3
"""
UserFeed utilities package

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
import sys
import time

# Third Party
from fastapi import HTTPException

# Internal
from .accounting_manager import store_in_iota
from .anonymizer import store_user_in_the_anonengine
from .logger import get_logger
from .position_alteration_detection import haversine
from .ublox_api import get_galileo_message, get_ublox_token, get_galileo_messages_list
from ..models.security import Authenticity
from ..models.user_feed.user import UserFeedInput, UserFeedOutput, PositionObject
from ..models.track import TrackSegmentsOutput


# --------------------------------------------------------------------------------------------


async def end_to_end_position_authentication(
        user_feed: UserFeedInput,
        timestamp: float,
        host: str,
        journey_id: str = "TEST",
        source_app: str = "TEST",
        client_id: str = "TEST",
        user_id: str = "TEST",
        test: bool = False
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
    :param test: True if is requested by the test endpoint
    :return: data validated
    """

    # Get Logger
    logger = get_logger()

    # Initialize
    galileo_auth_number = 0
    authentic_number = 0
    not_authentic_number = 0
    unknown_number = 0

    # Get Ublox-APi token
    ublox_token = await get_ublox_token()

    # Contact Ublox-Api for every position
    for position in user_feed.trace_information:
        # Find the location of the position (Sweden or Italy)
        location = haversine(position.lat, position.lon)

        for auth in position.galileo_auth:

            galileo_auth_number += 1
            try:
                galileo_data = await get_galileo_message(
                    auth.svid,
                    auth.time,
                    ublox_token,
                    location
                )
            except HTTPException as exc:
                if test is False:
                    await store_in_iota(
                        source_app=source_app,
                        client_id=client_id,
                        user_id=user_id,
                        msg_id=journey_id,
                        msg_size=0,
                        msg_time=timestamp,
                        msg_malicious_position=0,
                        msg_authenticated_position=0,
                        msg_unknown_position=0,
                        msg_total_position=0,
                        msg_error=True,
                        msg_error_description=exc.detail
                    )
                raise exc

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

                try:
                    # Remake the request
                    galileo_data_list = await get_galileo_messages_list(
                        auth.svid,
                        auth.time,
                        ublox_token,
                        location
                    )
                except HTTPException as exc:
                    if test is False:
                        await store_in_iota(
                            source_app=source_app,
                            client_id=client_id,
                            user_id=user_id,
                            msg_id=journey_id,
                            msg_size=0,
                            msg_time=timestamp,
                            msg_malicious_position=0,
                            msg_authenticated_position=0,
                            msg_unknown_position=0,
                            msg_total_position=0,
                            msg_error=True,
                            msg_error_description=exc.detail
                        )
                    raise exc
                for data in galileo_data_list:
                    if data.raw_data == auth.data:
                        position.authenticity = Authenticity.authentic
                        authentic_number += 1
                        not_authentic_number -= 1
                        break
                if position.authenticity == Authenticity.not_authentic:
                    await logger.warning(
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

    await logger.debug(
        {
            "host": host,
            "source_app": source_app,
            "journey_id": journey_id,
            "galileo_auth": galileo_auth_number,
            "authentic": authentic_number,
            "not_authentic": not_authentic_number,
            "unknown": unknown_number,
            "analysis_time": f"{time.time() - timestamp}"
        }
    )

    if test is False:
        await store_in_iota(
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

    return user_feed


async def store_android_data(
        user_feed_input: UserFeedInput,
        timestamp: float,
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
        user_feed_output = UserFeedOutput.construct(
            **{
                "app_defined_behaviour": user_feed.behaviour.app_defined,
                "tpv_defined_behaviour": user_feed.behaviour.tpv_defined,
                "user_defined_behaviour": [
                    TrackSegmentsOutput.construct(
                        **{
                            "start": PositionObject.construct(
                                **{
                                    "authenticity": behaviour.start.authenticity,
                                    "lat": behaviour.start.lat,
                                    "lon": behaviour.start.lon,
                                    "partialDistance": behaviour.start.partialDistance,
                                    "time": behaviour.start.time
                                }
                            ),
                            "meters": behaviour.meters,
                            "end": PositionObject.construct(
                                **{
                                    "authenticity": behaviour.end.authenticity,
                                    "lat": behaviour.end.lat,
                                    "lon": behaviour.end.lon,
                                    "partialDistance": behaviour.end.partialDistance,
                                    "time": behaviour.end.time
                                }
                            ),
                            "type": behaviour.type,
                        }
                    )
                    for behaviour in user_feed.behaviour.user_defined
                ],
                "company_code": user_feed.company_code,
                "company_trip_type": user_feed.company_trip_type,
                "deviceId": user_feed.id,
                "journeyId": journey_id,
                "startDate": user_feed.startDate,
                "endDate": user_feed.endDate,
                "distance": user_feed.distance,
                "elapsedTime": user_feed.elapsedTime,
                "positions": [
                    PositionObject.construct(
                        **{
                            "authenticity": position.authenticity,
                            "lat": position.lat,
                            "lon": position.lon,
                            "partialDistance": position.partialDistance,
                            "time": position.time
                        }
                    )
                    for position in user_feed.trace_information
                ],
                "sensors": user_feed.sensors_information,
                "mainTypeSpace": user_feed.mainTypeSpace,
                "mainTypeTime": user_feed.mainTypeTime,
                "sourceApp": source_app
            }
        )
        await store_user_in_the_anonengine(user_feed_output.dict())
    finally:
        return
