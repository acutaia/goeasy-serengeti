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
from ..config import UbloxApiSettings
from ..models.security import Token
from ..models.galileo.ublox_api import UbloxAPI, UbloxAPIList

# --------------------------------------------------------------------------------------------


async def get_ublox_token(settings: UbloxApiSettings) -> str:
    """
    Obtain a valid token to communicate with Ublox-Api

    :param settings: UbloxApi settings
    :return: UbloxApi valid token
    """
    # Get Logger
    logger = get_logger()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=settings.token_request_url,
                data={
                    "client_id": settings.client_id,
                    "username": settings.username_keycloak,
                    "password": settings.password,
                    "grant_type": settings.grant_type,
                    "client_secret": settings.client_secret
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
                        "client_id": settings.client_id,
                        "username": settings.username_keycloak,
                        "password": settings.password,
                        "grant_type": settings.grant_type,
                        "client_secret": settings.client_secret,
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
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        url: str,
        settings: UbloxApiSettings
) -> Optional[str]:
    """
    Contacts Ublox-Api and extracts raw data from the given satellite id and timestamp.

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :param settings: Ublox-Api settings
    :return:  The message
    """
    # Get Logger
    logger = get_logger()

    try:
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
            ublox_token = await get_ublox_token(settings)

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
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> Optional[str]:
    """
    Extract a Galileo Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Sweden or Italy
    :return: Galileo Message
    """

    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_galileo_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_galileo_uri}"

    return await _get_raw_data(
        client=client,
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=url,
        settings=settings
    )


async def get_ublox_message(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> Optional[str]:
    """
    Extract a Ublox Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Sweden or Italy
    :return: Galileo Message
    """

    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_ublox_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_ublox_uri}"

    return await _get_raw_data(
        client=client,
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=url,
        settings=settings
    )

# ---------------------------------------------------------------------------------------


async def _get_ublox_api_list(
        client: httpx.AsyncClient,
        ublox_token: str,
        url: str,
        data: dict,
        settings: UbloxApiSettings
) -> List[UbloxAPI]:
    """
    Contacts Ublox-Api and extracts a list of UbloxApi data format (timestamps and associated raw_data)
    for a specific satellite.

    :param client: Asynchronous Http client
    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :param data: asked data
    :param settings: Ublox-Api settings
    :return: list of UbloxApi objects
    """

    # Get logger
    logger = get_logger()

    try:
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
            ublox_token = await get_ublox_token(settings)

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
        window: int,
        window_step: int
) -> dict:
    """
    Constructs the dict of the request that will be made to Ublox-Api to retrieve the data of interest

    :param svid: Satellite Identifier
    :param timestamp: Timestamp associated to the measure
    :param window: window of timestamp
    :param window_step: step of the requested timestamps
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
                timestamp - window,
                timestamp + window + 1,
                window_step
            )
            if time != timestamp
        ]
    }


async def get_galileo_messages_list(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Galileo Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Could be Italy or Sweden
    :return: A list of Galileo Messages
    """

    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_galileo_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_galileo_uri}"

    return await _get_ublox_api_list(
        client=client,
        ublox_token=ublox_token,
        url=url,
        data=construct_request(svid, timestamp, settings.window, settings.window_step),
        settings=settings
    )


async def get_ublox_messages_list(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Ublox Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Could be Italy or Sweden
    :return: A list of Ublox Messages
    """

    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_ublox_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_ublox_uri}"

    return await _get_ublox_api_list(
        client=client,
        ublox_token=ublox_token,
        url=url,
        data=construct_request(svid, timestamp, settings.window, settings.window_step),
        settings=settings
    )
