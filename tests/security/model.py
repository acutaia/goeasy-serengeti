#!/usr/bin/env python3
"""
Security Models

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0
..

    Copyright 2021 LINKS Foundation

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
from enum import Enum
from datetime import datetime, timedelta
from typing import List

# Third PArty
from fastuuid import uuid4
from pydantic import Field

# Internal
from app.models.model import OrjsonModel
from .constants import ISSUER, AUDIENCE

# ----------------------------------------------------------------------------------


class Azp(str, Enum):
    get_token_client = "get_token_client"
    test = "Travis-ci/Test"


class UserName(str, Enum):
    goeasy_bq_library = "goeasy_bq_library"


class RolesEnum(str, Enum):
    inspect = "Inspect"
    admin = "Administration"
    auth = "Authenticate"
    test = "Test"
    user = "UserFeed"
    extract = "Extraction"
    iot = "IoTFeed"
    fake = "FakeToken"


class Roles(OrjsonModel):
    roles: List[RolesEnum] = [RolesEnum.test]


class Token(OrjsonModel):
    jti: str = str(uuid4())
    exp: datetime = datetime.utcnow() + timedelta(seconds=300)
    nbf: int = 0
    iat: datetime = datetime.utcnow() + timedelta(seconds=0.5)
    iss: str = ISSUER
    aud: str = AUDIENCE
    sub: str = str(uuid4())
    typ: str = "Bearer"
    azp: str = Field(...)
    auth_time: int = 0
    session_state: str = str(uuid4())
    acr: int = 1
    client_session: str = str(uuid4())
    allowed_origins: list = []
    realm_access: Roles
    resource_access: dict = {"roles": ["Testing"]}
    name: str = ""
