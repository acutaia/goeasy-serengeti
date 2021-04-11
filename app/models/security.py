#!/usr/bin/env python3
"""
Security models

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
from typing import Optional
from enum import IntEnum

# Internal
from .model import OrjsonModel

# ---------------------------------------------------------------


class Requester(OrjsonModel):
    """Requester Model"""

    client: str
    user: Optional[str]


# ---------------------------------------------------------------


class Token(OrjsonModel):
    """Token obtained from Keycloak"""

    access_token: str


# ---------------------------------------------------------------


class Authenticity(IntEnum):
    """Authenticity of the message"""

    authentic = 1
    unknown = -1
    not_authentic = 0
