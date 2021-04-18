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
from asyncio import Semaphore
import sys
import time

# Third Party
from fastapi import HTTPException

# Internal
from .accounting_manager import store_in_iota
from .ipt_anonymizer import store_in_the_anonymizer, SETTINGS
from .keycloak import KEYCLOACK
from .logger import get_logger
from .sessions.ublox_api import get_ublox_api_session
from .position_alteration_detection import haversine
from .ublox_api import get_ublox_message, get_ublox_messages_list
from ..concurrency.position_authentication import position_auth
from ..models.iot_feed.iot import IotInput
from ..models.security import Authenticity


# --------------------------------------------------------------------------------------------


async def end_to_end_position_authentication(
    iot_input: IotInput,
    timestamp: float,
    host: str,
    source_app: str = "TEST",
    client_id: str = "TEST",
    user_id: str = "TEST",
    obesrvation_gepid: str = "TEST",
    store: bool = False,
) -> dict:
    """
    Contact Ublox-API and validate IoT data

    :param iot_input: data to validate
    :param timestamp: when the request was received
    :param host: who made the request
    :param source_app: app that made the request
    :param client_id: client_id expressed by the token
    :param user_id: user_id expressed by the token
    :param obesrvation_gepid: uuid4 associated to the observation
    :param store: flag used to store data
    :return: data validated
    """
    # Get Logger
    logger = get_logger()
    # start analysis time
    start_analysis = time.time()
    # Extract position location
    location = haversine(
        iot_input.result.Position.coordinate[0], iot_input.result.Position.coordinate[1]
    )

    # Initialize
    galileo_auth_number = 0
    authentic_number = 0
    not_authentic_number = 0
    unknown_number = 0

    # Get Ublox-APi token
    ublox_token = await KEYCLOACK.get_ublox_token()

    # Get Ublox-Api session
    async with get_ublox_api_session() as session:

        # Calculate timestamp
        iot_time = int(iot_input.phenomenonTime.timestamp() * 1000)

        # Check the positions
        for gnss in iot_input.result.gnss:
            galileo_auth_number += 1

            try:
                galileo_data = await get_ublox_message(
                    gnss.svid, iot_time, ublox_token, location, session
                )
            except HTTPException as exc:
                if store:
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
                        msg_error_description=exc.detail,
                    )
                    galileo_data = None
                else:
                    raise exc

            if galileo_data is None:
                unknown_number += 1

            elif galileo_data == gnss.raw_data:
                authentic_number += 1

            else:
                not_authentic_number += 1
                not_authentic = True
                analyze = True

                try:
                    # Remake the request
                    galileo_data_list = await get_ublox_messages_list(
                        gnss.svid, iot_time, ublox_token, location, session
                    )
                except HTTPException as exc:
                    if store:
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
                            msg_error_description=exc.detail,
                        )
                        analyze = False
                    else:
                        raise exc

                if analyze:
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
                                    ublox_api.dict() for ublox_api in galileo_data_list
                                ],
                            }
                        )
                break

    if not_authentic_number > 0:
        authenticity = Authenticity.not_authentic
    elif authentic_number > 0:
        authenticity = Authenticity.authentic
    else:
        authenticity = Authenticity.unknown

    await logger.info(
        {
            "host": host,
            "observationGEPid": obesrvation_gepid,
            "galileo_auth": galileo_auth_number,
            "authentic": authentic_number,
            "not_authentic": not_authentic_number,
            "unknown": unknown_number,
            "analysis_time": f"{time.time() - start_analysis}",
            "request_procession_time": f"{time.time() - timestamp}",
        }
    )
    if store:
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
            msg_total_position=galileo_auth_number,
        )

    iot_output = iot_input.dict(exclude={"result": {"gnss"}})
    iot_output["result"].update({"authenticity": authenticity})
    iot_output.update({"observationGEPid": obesrvation_gepid})

    return iot_output


async def store_iot_data(
    iot_input: IotInput,
    timestamp: float,
    host: str,
    obesrvation_gepid: str,
    source_app: str,
    client_id: str,
    user_id: str,
    semaphore: Semaphore,
) -> None:
    """
    Store IoT data in the anonymizer

    :param iot_input: data to validate
    :param timestamp: when the request was received
    :param host: who made the request
    :param obesrvation_gepid: uuid4 associated to the request
    :param source_app: app that made the request
    :param client_id: client_id expressed by the token
    :param user_id: user_id expressed by the token
    :param semaphore: synchronize the requests and prevent starvation
    """
    try:
        async with semaphore:
            async with position_auth():
                iot_output = await end_to_end_position_authentication(
                    iot_input=iot_input,
                    timestamp=timestamp,
                    host=host,
                    obesrvation_gepid=obesrvation_gepid,
                    source_app=source_app,
                    client_id=client_id,
                    user_id=user_id,
                    store=True,
                )

            await store_in_the_anonymizer(iot_output, SETTINGS.store_iot_data_url)
    finally:
        return
