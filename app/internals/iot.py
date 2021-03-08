#!/usr/bin/env python3
"""
IoT utilities package

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
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
import time
import sys

# Third Party
import httpx
from fastapi import HTTPException

# Internal
from .logger import get_logger
from .accounting_manager import store_in_iota
from .position_alteration_detection import haversine
from .ublox_api import get_ublox_message, get_ublox_token, get_ublox_messages_list
from ..models.iot_feed.iot import IotInput, IotOutput, ResultOutput
from ..models.security import Authenticity
from ..config import get_ublox_api_settings


# --------------------------------------------------------------------------------------------


async def end_to_end_position_authentication(
        iot_input: IotInput,
        timestamp: float,
        host: str,
        source_app: str,
        client_id: str,
        user_id: str,
        obesrvation_gepid: str
) -> IotOutput:
    """
    Contact Ublox-API and validate IoT data

    :param iot_input: data to validate
    :param timestamp: when the request was received
    :param host: who made the request
    :param source_app: app that made the request
    :param client_id: client_id expressed by the token
    :param user_id: user_id expressed by the token
    :param obesrvation_gepid: uuid4 associated to the observation
    :return: data validated
    """
    # Get Logger
    logger = get_logger()
    # Get Ublox-APi token and settings
    ublox_api_settings = get_ublox_api_settings()
    ublox_token = await get_ublox_token(ublox_api_settings)

    # Extract timestamp
    iot_time = int(iot_input.phenomenonTime.timestamp()*1000)

    # Extract position location
    location = haversine(
        iot_input.result.Position.coordinate[0],
        iot_input.result.Position.coordinate[1]
    )

    # Initialize
    galileo_auth_number = 0
    authentic_number = 0
    not_authentic_number = 0
    unknown_number = 0

    async with httpx.AsyncClient(verify=False) as client:
        for gnss in iot_input.result.gnss:
            galileo_auth_number += 1

            try:
                galileo_data = await get_ublox_message(
                    client,
                    gnss.svid,
                    iot_time,
                    ublox_token,
                    ublox_api_settings,
                    location
                )
            except HTTPException as exc:
                await store_in_iota(
                        source_app=source_app,
                        client_id=client_id,
                        user_id=user_id,
                        msg_id=obesrvation_gepid,
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
                unknown_number += 1

            elif galileo_data == gnss.raw_data:
                authentic_number += 1

            else:
                not_authentic_number += 1
                not_authentic = True

                try:
                    # Remake the request
                    galileo_data_list = await get_ublox_messages_list(
                        client,
                        gnss.svid,
                        iot_time,
                        ublox_token,
                        ublox_api_settings,
                        location
                    )
                except HTTPException as exc:
                    await store_in_iota(
                            source_app=source_app,
                            client_id=client_id,
                            user_id=user_id,
                            msg_id=obesrvation_gepid,
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
                    if data.raw_data == gnss.raw_data:
                        authentic_number += 1
                        not_authentic_number -= 1
                        not_authentic = False
                        break

                if not_authentic:
                    await logger.warning(
                        {
                            "message_timestamp": iot_time,
                            "ublox_message": gnss.raw_data,
                            "satellite_id": gnss.svid,
                            "status": "Real Fake",
                            "ublox_api_messages": [
                                ublox_api.dict()
                                for ublox_api in galileo_data_list
                            ]
                        }
                    )
                break

    if not_authentic_number > 0:
        authenticity = Authenticity.not_authentic
    elif authentic_number > 0:
        authenticity = Authenticity.authentic
    else:
        authenticity = Authenticity.unknown

    await logger.debug(
        {
            "host": host,
            "observationGEPid": obesrvation_gepid,
            "galileo_auth": galileo_auth_number,
            "authentic": authentic_number,
            "not_authentic": not_authentic_number,
            "unknown": unknown_number,
            "analysis_time": f"{time.time() - timestamp}"
        }
    )

    await store_in_iota(
            source_app=source_app,
            client_id=client_id,
            user_id=user_id,
            msg_id=obesrvation_gepid,
            msg_size=sys.getsizeof(iot_input.json()),
            msg_time=timestamp,
            msg_malicious_position=not_authentic_number,
            msg_authenticated_position=authentic_number,
            msg_unknown_position=unknown_number,
            msg_total_position=galileo_auth_number

        )

    iot_input_dict = iot_input.dict()
    iot_input_dict["result"] = ResultOutput(
        valueType=iot_input.result.valueType,
        Position=iot_input.result.Position,
        response=iot_input.result.response,
        authenticity=authenticity
    ).dict()
    iot_input_dict.update({"observationGEPid": obesrvation_gepid})

    return IotOutput.construct(**iot_input_dict)
