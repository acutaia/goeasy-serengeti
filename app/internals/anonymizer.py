#!/usr/bin/env python3
"""
Anonymizer package

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

# Standard library
from typing import Any

# Third Party
from fastapi import status, HTTPException
import httpx
import orjson

# Internal
from .logger import get_logger
from .session import get_anonymizer_session
from ..config import get_anonymizer_settings

# --------------------------------------------------------------------------------------------


async def store_in_the_anonengine(data: dict, url: str) -> None:
    """
    Store user info in the anonengine

    :param data: User information to store in the anonengine
    :param url: could be iot or user
    """
    # Get Logger
    logger = get_logger()
    # Get anonymizer settings
    anonymizer_settings = get_anonymizer_settings()
    # Store data
    try:
        client = get_anonymizer_session()
        response = await client.post(
            getattr(anonymizer_settings, url),
            data=data,
            timeout=10
        )
        await logger.debug(orjson.loads(response.content))
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
            detail="Can't contact Anonymizer service"
        )

# --------------------------------------------------------------------------------------------


async def _extract(url: str) -> Any:
    """
    Extract info from the anonengine

    :param url: requested info
    :return: Info
    """

    # Get Logger
    logger = get_logger()

    try:
        client = get_anonymizer_session()
        response = await client.get(url, timeout=25)

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
            detail="Can't contact Anonymizer service"
        )
    return orjson.loads(response.content)

# --------------------------------------------------------------------------------------------


async def extract_mobility(journey_id: str) -> Any:
    """
    Extract mobility info from the anonengine

    :param journey_id: Requested journey id
    """
    settings = get_anonymizer_settings()
    return await _extract(f"{settings.get_mobility_url}/{journey_id}")

# --------------------------------------------------------------------------------------------


async def extract_details(journey_id: str) -> Any:
    """
    Extract details from the anonengine

    :param journey_id: Requested journey id
    """
    settings = get_anonymizer_settings()
    return await _extract(f"{settings.get_details_url}/{journey_id}")
