#!/usr/bin/env python3
"""
Background concurrency

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
from asyncio import Semaphore, TimeoutError, wait_for

# Third Party
from fastapi import HTTPException, status

# --------------------------------------------------------------------------------------------


async def frequency_limiter(sem: Semaphore) -> None:
    """
    Function that must be used only inside router module
    to wait some time before answer to the client and let the background task to start

    :param sem: semaphore to store iot or user data
    """
    try:
        await wait_for(sem.acquire(), 5)
        sem.release()

    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

