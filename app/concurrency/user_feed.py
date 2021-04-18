#!/usr/bin/env python3
"""
User feed concurrency

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


@dataclass(repr=False, eq=False)
class _UserFeedSemaphore:
    store: Semaphore
    test: Semaphore


@lru_cache(maxsize=1)
def _get_user_semaphore() -> _UserFeedSemaphore:
    return _UserFeedSemaphore(store=Semaphore(40), test=Semaphore(2))


@lru_cache(maxsize=1)
def store_semaphore() -> Semaphore:
    """Synchronize user store requests to prevent starvation"""
    return _get_user_semaphore().store


@lru_cache(maxsize=1)
def test_semaphore() -> Semaphore:
    """Synchronize user test requests to prevent starvation"""
    return _get_user_semaphore().test
