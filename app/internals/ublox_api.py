#!/usr/bin/env python3
"""
Ublox-Api package

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
from typing import Optional, List

# Third Party
from fastapi import status, HTTPException
import httpx

# Internal
from .logger import get_logger
from .session import get_keycloack_session, get_ublox_api_session
from ..config import get_ublox_api_settings
from ..models.security import Token
from ..models.galileo.ublox_api import UbloxAPI, UbloxAPIList

# --------------------------------------------------------------------------------------------

SETTINGS = get_ublox_api_settings()
""" Ublox-Api settings """

URL_UBLOX = {
    "Italy": f"{SETTINGS.ublox_api_italy_ip}{SETTINGS.ublox_api_ublox_uri}",
    "Sweden": f"{SETTINGS.ublox_api_sweden_ip}{SETTINGS.ublox_api_ublox_uri}"
}
""" Italian and Swedish url for getting ublox messages """

URL_GALILEO = {
    "Italy": f"{SETTINGS.ublox_api_italy_ip}{SETTINGS.ublox_api_galileo_uri}",
    "Sweden": f"{SETTINGS.ublox_api_sweden_ip}{SETTINGS.ublox_api_galileo_uri}"
}
""" Italian and Swedish url for getting galileo messages """

# --------------------------------------------------------------------------------------------


async def get_ublox_token() -> str:
    """
    Obtain a valid token to communicate with Ublox-Api

    :return: UbloxApi valid token
    """
    # Get Logger
    logger = get_logger()

    try:
        client = get_keycloack_session()
        response = await client.post(
            url=SETTINGS.token_request_url,
            data={
                "client_id": SETTINGS.client_id,
                "username": SETTINGS.username_keycloak,
                "password": SETTINGS.password,
                "grant_type": SETTINGS.grant_type,
                "client_secret": SETTINGS.client_secret
            },
            timeout=25
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:

            # Credentials Wrong
            await logger.error(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "client_id": SETTINGS.client_id,
                    "username": SETTINGS.username_keycloak,
                    "password": SETTINGS.password,
                    "grant_type": SETTINGS.grant_type,
                    "client_secret": SETTINGS.client_secret,
                    "status_code": exc.response.status_code,
                    "error": exc
                }
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong credentials"
            )
    except httpx.RequestError as exc:

        # Can't contact keycloack
        await logger.warning(
            {
                "method": exc.request.method,
                "url": exc.request.url,
                "error": exc
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Keycloack service"
        )

    return Token.parse_raw(response.content).access_token

# --------------------------------------------------------------------------------------------


async def _get_raw_data(
        svid: int,
        timestamp: int,
        ublox_token: str,
        url: str,
) -> Optional[str]:
    """
    Contacts Ublox-Api and extracts raw data from the given satellite id and timestamp.

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :return:  The message
    """
    # Get Logger
    logger = get_logger()

    try:
        client = get_ublox_api_session()
        response = await client.get(
            f"{url}/{svid}/{timestamp}",
            headers={
                "Authorization": f"Bearer {ublox_token}"
            },
            timeout=10
        )
        try:
            # Check if the token is expired
            response.raise_for_status()
            return UbloxAPI.parse_raw(response.content).raw_data

        except httpx.HTTPStatusError as exc:

            # Token is expired
            await logger.warning(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "token": ublox_token,
                    "status_code": exc.response.status_code,
                    "error": exc
                }
            )
            # Get new Token
            ublox_token = await get_ublox_token()

            # Remake the request
            response = await client.get(
                f"{url}/{svid}/{timestamp}",
                headers={
                    "Authorization": f"Bearer {ublox_token}"
                },
                timeout=10
            )
            return UbloxAPI.parse_raw(response.content).raw_data

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        await logger.error(
            {
                "method": exc.request.method,
                "url": exc.request.url,
                "error": exc
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Ublox-Api service"
        )


async def get_galileo_message(
        svid: int,
        timestamp: int,
        ublox_token: str,
        location: str
) -> Optional[str]:
    """
    Extract a Galileo Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Sweden or Italy
    :return: Galileo Message
    """

    return await _get_raw_data(
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=URL_GALILEO[location],
    )


async def get_ublox_message(
        svid: int,
        timestamp: int,
        ublox_token: str,
        location: str
) -> Optional[str]:
    """
    Extract a Ublox Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Sweden or Italy
    :return: Galileo Message
    """

    return await _get_raw_data(
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=URL_UBLOX[location],
    )

# ---------------------------------------------------------------------------------------


async def _get_ublox_api_list(
        ublox_token: str,
        url: str,
        data: dict,
) -> List[UbloxAPI]:
    """
    Contacts Ublox-Api and extracts a list of UbloxApi data format (timestamps and associated raw_data)
    for a specific satellite.

    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :param data: asked data
    :return: list of UbloxApi objects
    """

    # Get logger
    logger = get_logger()

    try:
        client = get_ublox_api_session()
        response = await client.post(
            url,
            json=data,
            headers={
                "Authorization": f"Bearer {ublox_token}",
            },
            timeout=10
        )
        try:
            response.raise_for_status()
            return UbloxAPIList.parse_raw(response.content).info

        except httpx.HTTPStatusError as exc:
            # Token is expired
            await logger.warning(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "token": ublox_token,
                    "status_code": exc.response.status_code,
                    "error": exc
                }
            )
            # Get new Token
            ublox_token = await get_ublox_token()

            # Remake the request
            response = await client.post(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {ublox_token}",
                },
                timeout=10
            )
            return UbloxAPIList.parse_raw(response.content).info

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        await logger.error(
            {
                "method": exc.request.method,
                "url": exc.request.url,
                "token": ublox_token,
                "error": exc
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Ublox-Api service"
        )


def construct_request(
        svid: int,
        timestamp: int,
) -> dict:
    """
    Constructs the dict of the request that will be made to Ublox-Api to retrieve the data of interest

    :param svid: Satellite Identifier
    :param timestamp: Timestamp associated to the measure
    :return: Data to ask to Ublox-Api
    """
    return {
        "satellite_id": svid,
        "info": [
            {
                "timestamp": time,
                "raw_data": None
            }
            for time in range(
                timestamp - SETTINGS.window,
                timestamp + SETTINGS.window + 1,
                SETTINGS.window_step
            )
            if time != timestamp
        ]
    }


async def get_galileo_messages_list(
        svid: int,
        timestamp: int,
        ublox_token: str,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Galileo Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Could be Italy or Sweden
    :return: A list of Galileo Messages
    """

    return await _get_ublox_api_list(
        ublox_token=ublox_token,
        url=URL_GALILEO[location],
        data=construct_request(svid, timestamp)
    )


async def get_ublox_messages_list(
        svid: int,
        timestamp: int,
        ublox_token: str,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Ublox Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Could be Italy or Sweden
    :return: A list of Ublox Messages
    """

    return await _get_ublox_api_list(
        ublox_token=ublox_token,
        url=URL_UBLOX[location],
        data=construct_request(svid, timestamp)
    )
