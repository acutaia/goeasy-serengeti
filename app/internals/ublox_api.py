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
from asyncio import TimeoutError
from typing import Optional, List

# Third Party
from aiohttp import ClientSession, ClientResponseError
from fastapi import status, HTTPException
import orjson

# Internal
from .keycloak import KEYCLOACK
from .logger import get_logger
from ..config import get_ublox_api_settings
from ..models.galileo.ublox_api import UbloxAPI, UbloxAPIList

# --------------------------------------------------------------------------------------------

SETTINGS = get_ublox_api_settings()
""" Ublox-Api settings """

URL_UBLOX = {
    "Italy": f"{SETTINGS.ublox_api_italy_ip}{SETTINGS.ublox_api_ublox_uri}",
    "Sweden": f"{SETTINGS.ublox_api_sweden_ip}{SETTINGS.ublox_api_ublox_uri}",
}
""" Italian and Swedish url for getting ublox messages """

URL_GALILEO = {
    "Italy": f"{SETTINGS.ublox_api_italy_ip}{SETTINGS.ublox_api_galileo_uri}",
    "Sweden": f"{SETTINGS.ublox_api_sweden_ip}{SETTINGS.ublox_api_galileo_uri}",
}
""" Italian and Swedish url for getting galileo messages """

# --------------------------------------------------------------------------------------------


async def _get_raw_data(
    svid: int,
    timestamp: int,
    ublox_token: str,
    url: str,
    session: ClientSession,
) -> Optional[str]:
    """
    Contacts Ublox-Api and extracts raw data from the given satellite id and timestamp.

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :param session: Aiohttp session
    :return:  The message
    """
    # Get Logger
    logger = get_logger()

    try:
        async with session.get(
            f"{url}/{svid}/{timestamp}",
            headers={"Authorization": f"Bearer {ublox_token}"},
        ) as resp:
            # Return RawData
            return UbloxAPI.parse_obj(
                await resp.json(encoding="utf-8", loads=orjson.loads, content_type=None)
            ).raw_data

    except ClientResponseError as exc:
        # Token is expired
        await logger.warning(
            {
                "method": exc.request_info.method,
                "url": exc.request_info.url,
                "token": ublox_token,
                "status_code": exc.status,
                "error": exc.message,
            }
        )
        # Get new Token
        ublox_token = await KEYCLOACK.get_ublox_token()

        # Remake the request
        async with session.get(
            f"{url}/{svid}/{timestamp}",
            headers={"Authorization": f"Bearer {ublox_token}"},
        ) as resp:
            # Return RawData
            return UbloxAPI.parse_obj(
                await resp.json(encoding="utf-8", loads=orjson.loads, content_type=None)
            ).raw_data

    except TimeoutError:
        # Ublox-Api is in starvation
        await logger.warning({"error": "Ublox-Api is in starvation"})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ublox-Api service unavailable",
        )


async def get_galileo_message(
    svid: int,
    timestamp: int,
    ublox_token: str,
    location: str,
    session: ClientSession,
) -> Optional[str]:
    """
    Extract a Galileo Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Sweden or Italy
    :param session: Aiohttp session
    :return: Galileo Message
    """

    return await _get_raw_data(
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=URL_GALILEO[location],
        session=session,
    )


async def get_ublox_message(
    svid: int, timestamp: int, ublox_token: str, location: str, session: ClientSession
) -> Optional[str]:
    """
    Extract a Ublox Message from a specific Ublox-Api server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Sweden or Italy
    :param session: Aiohttp session
    :return: Galileo Message
    """

    return await _get_raw_data(
        svid=svid,
        timestamp=timestamp,
        ublox_token=ublox_token,
        url=URL_UBLOX[location],
        session=session,
    )


# ---------------------------------------------------------------------------------------


async def _get_ublox_api_list(
    ublox_token: str, url: str, data: dict, session: ClientSession
) -> List[UbloxAPI]:
    """
    Contacts Ublox-Api and extracts a list of UbloxApi data format (timestamps and associated raw_data)
    for a specific satellite.

    :param ublox_token: Token to use with UbloxApi
    :param url: Url of Ublox-Api server, it could be in Italy or Sweden
    :param data: asked data
    :param session: Aiohttp session
    :return: list of UbloxApi objects
    """

    # Get logger
    logger = get_logger()

    try:
        async with session.post(
            url=url,
            json=data,
            headers={
                "Authorization": f"Bearer {ublox_token}",
            },
        ) as resp:
            # Return Info requested
            return UbloxAPIList.parse_obj(
                await resp.json(encoding="utf-8", loads=orjson.loads, content_type=None)
            ).info

    except ClientResponseError as exc:
        # Token is expired
        await logger.warning(
            {
                "method": exc.request_info.method,
                "url": exc.request_info.url,
                "token": ublox_token,
                "status_code": exc.status,
                "error": exc.message,
            }
        )
        # Get new Token
        ublox_token = await KEYCLOACK.get_ublox_token()

        # Remake the request
        async with session.post(
            url=url,
            json=data,
            headers={
                "Authorization": f"Bearer {ublox_token}",
            },
        ) as resp:
            # Return Info requested
            return UbloxAPIList.parse_obj(
                await resp.json(encoding="utf-8", loads=orjson.loads, content_type=None)
            ).info

    except TimeoutError:
        # Ublox-Api is in starvation
        await logger.warning({"error": "Ublox-Api is in starvation"})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ublox-Api service unavailable",
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
            {"timestamp": time, "raw_data": None}
            for time in range(
                timestamp - SETTINGS.window,
                timestamp + SETTINGS.window + 1,
                SETTINGS.window_step,
            )
            if time != timestamp
        ],
    }


async def get_galileo_messages_list(
    svid: int,
    timestamp: int,
    ublox_token: str,
    location: str,
    session: ClientSession,
) -> List[UbloxAPI]:
    """
    Extract a list of  Galileo Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Could be Italy or Sweden
    :param session: Aiohttp session
    :return: A list of Galileo Messages
    """

    return await _get_ublox_api_list(
        ublox_token=ublox_token,
        url=URL_GALILEO[location],
        data=construct_request(svid, timestamp),
        session=session,
    )


async def get_ublox_messages_list(
    svid: int, timestamp: int, ublox_token: str, location: str, session: ClientSession
) -> List[UbloxAPI]:
    """
    Extract a list of  Ublox Messages in a range of timestamps from a specific Ublox-Api
    server situated in Italy or in Sweden

    :param svid: Satellite identifier
    :param timestamp: Requested timestamp
    :param ublox_token: Token to use with UbloxApi
    :param location: Could be Italy or Sweden
    :param session: Aiohttp session
    :return: A list of Ublox Messages
    """

    return await _get_ublox_api_list(
        ublox_token=ublox_token,
        url=URL_UBLOX[location],
        data=construct_request(svid, timestamp),
        session=session,
    )
