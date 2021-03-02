#!/usr/bin/env python3
"""
Anonymizer package

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

# Third Party
from aiologger.loggers.json import JsonLogger
from fastapi import status, HTTPException
import httpx
import orjson

# Internal
from ..config import get_anonymizer_settings

logger = JsonLogger.with_default_handlers(
    name="anonymizer",
    serializer_kwargs={"indent": 4}
)

# --------------------------------------------------------------------------------------------


async def store_user_in_the_anonengine(user_feed: bytes) -> None:
    """
    Store user info in the anonengine

    :param user_feed: User information to store in the anonengine
    """
    # Get anonymizer settings
    anonymizer_settings = get_anonymizer_settings()
    # Store data
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                anonymizer_settings.store_data_url,
                data=user_feed
            )
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
            detail="Can't contact Anonymizer service"
        )

# --------------------------------------------------------------------------------------------


async def extract_mobility(journey_id: str) -> str:
    """
    Extract mobility info from the anonengine

    :param journey_id: Requested journey id
    """
    settings = get_anonymizer_settings()

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{settings.get_mobility_url}/{journey_id}")

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
                detail="Can't contact Anonymizer service"
            )
    return orjson.loads(response.content)

# --------------------------------------------------------------------------------------------


async def extract_details(journey_id: str) -> bytes:
    """
    Extract details from the anonengine

    :param journey_id: Requested journey id
    """

    settings = get_anonymizer_settings()

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{settings.get_details_url}/{journey_id}")

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
                detail="Can't contact Anonymizer service"
            )
    return orjson.loads(response.content)
