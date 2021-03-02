#!/usr/bin/env python3
"""
Ublox-Api package

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
from typing import Optional, List

# Third Party
from aiologger.loggers.json import JsonLogger
from fastapi import status, HTTPException
import httpx
import orjson

# Internal
from ..config import UbloxApiSettings
from ..models.security import Token
from ..models.galileo.ublox_api import UbloxAPI, UbloxAPIList

logger = JsonLogger.with_default_handlers(
    name="ublox-api",
    serializer_kwargs={"indent": 4}
)

# --------------------------------------------------------------------------------------------


async def get_ublox_token(settings: UbloxApiSettings) -> str:
    """
    Obtain a valid token to communicate with Ublox-Api

    :param settings: UbloxApi settings
    :return: UbloxApi valid token
    """
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
                }
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:

                # Credentials Wrong
                logger.error(
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
            logger.warning(
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


async def get_galileo_message(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> Optional[str]:
    """
    Extract a Galileo Message from Ublox-APi

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

    try:
        response = await client.get(
            f"{url}/{svid}/{timestamp}",
            headers={
                "Authorization": f"Bearer {ublox_token}"
            }
        )
        try:
            # Check if the token is expired
            response.raise_for_status()
            return UbloxAPI.parse_raw(response.content).raw_data

        except httpx.HTTPStatusError as exc:

            # Token is expired
            logger.warning(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "token": ublox_token,
                    "status_code": exc.response.status_code,
                    "error": exc
                }
            )
            # Get new Token
            ublox_token = await get_ublox_token(settings)  # get new Token

            # Remake the request
            response = await client.get(
                f"{url}/{svid}/{timestamp}",
                headers={
                    "Authorization": f"Bearer {ublox_token}"
                }
            )
            return UbloxAPI.parse_raw(response.content).raw_data

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        logger.error(
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


# ---------------------------------------------------------------------------------------


async def get_ublox_message(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> Optional[str]:
    """
    Extract a Galileo Message from Ublox-APi

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Sweden or Italy
    :return: Galileo Message
    """
    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_uri}"
    try:
        response = await client.get(
            f"{url}/{svid}/{timestamp}",
            headers={
                "Authorization": f"Bearer {ublox_token}"
            }
        )
        try:
            # Check if the token is expired
            response.raise_for_status()
            return UbloxAPI.parse_raw(response.content).raw_data

        except httpx.HTTPStatusError as exc:

            # Token is expired
            logger.warning(
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
                }
            )
            return UbloxAPI.parse_raw(response.content).raw_data

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        logger.error(
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

# ---------------------------------------------------------------------------------------


async def get_galileo_message_list(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Galileo Messages in a range of timestamps from Ublox-Api

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

    galileo_data_list_request = orjson.dumps(
        {
            "satellite_id": svid,
            "info": [
                {
                    "timestamp": time
                }
                for time in range(
                    timestamp - settings.window,
                    timestamp + settings.window + 1,
                    settings.window_step
                )
                if time != timestamp
            ]
        }
    )

    try:
        response = await client.post(
            url,
            data=galileo_data_list_request,
            headers={
                "Authorization": f"Bearer {ublox_token}",
            }
        )
        try:
            response.raise_for_status()
            return UbloxAPIList.parse_raw(response.content).info

        except httpx.HTTPStatusError as exc:
            # Token is expired
            logger.warning(
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
                data=galileo_data_list_request,
                headers={
                    "Authorization": f"Bearer {ublox_token}",
                }
            )
            return UbloxAPIList.parse_raw(response.content).info

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        logger.error(
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


async def get_ublox_message_list(
        client: httpx.AsyncClient,
        svid: int,
        timestamp: int,
        ublox_token: str,
        settings: UbloxApiSettings,
        location: str
) -> List[UbloxAPI]:
    """
    Extract a list of  Galileo Messages in a range of timestamps from Ublox-Api

    :param client: Asynchronous Http client
    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param settings: Ublox Api settings
    :param location: Could be Italy or Sweden
    :return: A list of Galileo Messages
    """

    if location == "Italy":
        url = f"{settings.ublox_api_italy_ip}{settings.ublox_api_uri}"

    else:
        url = f"{settings.ublox_api_sweden_ip}{settings.ublox_api_uri}"

    galileo_data_list_request = orjson.dumps(
        {
            "satellite_id": svid,
            "info": [
                {
                    "timestamp": time
                }
                for time in range(
                    timestamp - settings.window,
                    timestamp + settings.window + 1,
                    settings.window_step
                )
                if time != timestamp
            ]
        }
    )

    try:
        response = await client.post(
            url,
            data=galileo_data_list_request,
            headers={
                "Authorization": f"Bearer {ublox_token}",
            }
        )
        try:
            response.raise_for_status()
            return UbloxAPIList.parse_raw(response.content).info

        except httpx.HTTPStatusError as exc:
            # Token is expired
            logger.warning(
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
                data=galileo_data_list_request,
                headers={
                    "Authorization": f"Bearer {ublox_token}",
                }
            )
            return UbloxAPIList.parse_raw(response.content).info

    except httpx.RequestError as exc:
        # Something went wrong during the connection
        logger.error(
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

