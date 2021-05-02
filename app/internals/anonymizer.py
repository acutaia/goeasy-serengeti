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

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard library
from asyncio import TimeoutError
from typing import Any

# Third Party
from aiohttp import ClientError
from fastapi import status, HTTPException
import orjson

# Internal
from .logger import get_logger
from .sessions.anonymizer import get_anonengine_session
from ..config import get_anonymizer_settings

# --------------------------------------------------------------------------------------------


async def store_in_the_anonengine(data: dict) -> None:
    """
    Store user info in the anonengine

    :param data: User information to store in the anonengine
    """
    # Get Logger
    logger = get_logger()
    # Get anonymizer settings
    anonymizer_settings = get_anonymizer_settings()
    try:
        # Store data
        async with get_anonengine_session() as session:
            async with session.post(
                anonymizer_settings.store_data_url, json=data, timeout=0.5
            ):
                pass

    except (TimeoutError, ClientError) as exc:
        # Something went wrong during the connection
        await logger.info(
            {"url": anonymizer_settings.store_data_url, "error": repr(str(exc))}
        )
        return


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
        async with get_anonengine_session() as session:
            async with session.get(url, timeout=20) as resp:
                return await resp.json(
                    encoding="utf-8", loads=orjson.loads, content_type=None
                )

    except (TimeoutError, ClientError) as exc:
        # Something went wrong during the connection
        await logger.warning({"url": url, "error": repr(str(exc))})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Anonymizer service",
        )


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
