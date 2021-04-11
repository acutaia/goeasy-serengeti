#!/usr/bin/env python3
"""
IoT concurrency

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
from dataclasses import dataclass
from functools import lru_cache

# --------------------------------------------------------------------------------------------


@dataclass
class _IoTFeedSemaphore:
    store: Semaphore
    test: Semaphore


@lru_cache(maxsize=1)
def _get_iot_semaphore() -> _IoTFeedSemaphore:
    return _IoTFeedSemaphore(store=Semaphore(10), test=Semaphore(5))


@lru_cache(maxsize=1)
def store_semaphore() -> Semaphore:
    """synchronize iot store requests to prevent starvation"""
    return _get_iot_semaphore().store


@lru_cache(maxsize=1)
def test_semaphore() -> Semaphore:
    """synchronize iot test requests to prevent starvation"""
    return _get_iot_semaphore().test
