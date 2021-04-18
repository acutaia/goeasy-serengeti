#!/usr/bin/env python3
"""
Position Authentication concurrency

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
from asyncio import Semaphore
from functools import lru_cache

# --------------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def user_semaphore() -> Semaphore:
    """Synchronize user store requests to prevent starvation"""
    return Semaphore(40)

# --------------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def iot_semaphore() -> Semaphore:
    """synchronize iot store requests to prevent starvation"""
    return Semaphore(5)

# --------------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def position_auth() -> Semaphore:
    """Synchronize position authorization requests to prevent starvation"""
    return Semaphore(20)

# --------------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def position_test() -> Semaphore:
    """Synchronize position authorization requests to prevent starvation"""
    return Semaphore(2)
