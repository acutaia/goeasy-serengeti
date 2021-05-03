#!/usr/bin/env python3
"""
IPT-anonymizer package

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

# Standard Library
from asyncio import TimeoutError

# Third Party
from aiohttp import ClientError
from fastapi import status, HTTPException
import orjson

# Internal
from .logger import get_logger
from .sessions.ipt_anonymizer import ipt_anonymizer_session
from ..config import get_ipt_anonymizer_settings

# --------------------------------------------------------------------------------------------


SETTINGS = get_ipt_anonymizer_settings()
"""IPT-Anonymizer settings"""


async def store_in_the_anonymizer(data: dict, url: str) -> None:
    """
    Store user info in the IPT-anonymizer

    :param data: User information to store in the anonengine
    :param url: used to store iot or user data
    """
    # Get Logger
    logger = get_logger()

    # obtain the semaphore to prevent starvation
    try:
        # Store data
        async with ipt_anonymizer_session() as session:
            async with session.post(url=url, json=data, timeout=6):
                pass

    except (TimeoutError, ClientError) as exc:
        # IPT-anonymizer is in starvation
        await logger.warning({"url": url, "error": repr(str(exc))})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IPT-anonymizer is in starvation or down",
        )


# --------------------------------------------------------------------------------------------


async def extract_user_info(info_requested: dict) -> tuple:
    """
    Extract info from stored in the IPT-anonymizer

    :param info_requested: User information to store in the anonengine
    """
    # Get Logger
    logger = get_logger()

    try:
        # Extract data
        async with ipt_anonymizer_session() as session:
            async with session.post(
                url=SETTINGS.extract_user_data_url, json=info_requested, timeout=20
            ) as resp:
                return resp.status, await resp.json(
                    encoding="utf-8", loads=orjson.loads, content_type=None
                )

    except (TimeoutError, ClientError) as exc:
        # IPT-anonymizer is in starvation
        await logger.warning(
            {"url": SETTINGS.extract_user_data_url, "error": repr(str(exc))}
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IPT-anonymizer is in starvation or down",
        )
