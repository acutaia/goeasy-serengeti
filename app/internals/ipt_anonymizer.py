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

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


# Third Party
from asyncio import TimeoutError
from aiohttp import ClientError
from fastapi import status, HTTPException

# Internal
from .logger import get_logger
from .sessions.ipt_anonymizer import store_session
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
    # Get anonymizer settings
    anonymizer_settings = get_ipt_anonymizer_settings()

    try:
        # Store data
        session = store_session()
        async with session.post(url=url, json=data, timeout=5):
            pass

    except TimeoutError:
        # IPT-anonymizer is in starvation
        await logger.warning({"url": url, "error": "IPT-anonymizer is in starvation"})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IPT-anonymizer is in starvation",
        )
    except ClientError as exc:
        # IPT-anonymizer has some problems
        await logger.error({"url": url, "error": repr(str(exc))})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="IPT-anonymizer is in starvation",
        )


# --------------------------------------------------------------------------------------------
