#!/usr/bin/env python3
"""
Token security

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
from datetime import datetime, timedelta
from typing import Optional

# Third Party
from jose import jwt

# Internal
from app.config import get_security_settings
from .constants import PRIVATE_KEY, ISSUER, PUBLIC_KEY, AUDIENCE
from .model import Token, Azp, Roles, RolesEnum

# ------------------------------------------------------------------------------------------


def change_default_security_settings():
    """Change the default security settings for testing purpose"""
    settings = get_security_settings()
    settings.issuer = ISSUER
    settings.realm_public_key = PUBLIC_KEY
    settings.audience = AUDIENCE


def generate_fake_token() -> str:
    """
    Generate a fake token to ensure that the app is secure

    :return: token
    """
    to_encode = Token(
        exp=datetime.utcnow() - timedelta(seconds=300),
        iat=datetime.utcnow() - timedelta(seconds=301),
        azp=Azp.test,
        realm_access=Roles(roles=[RolesEnum.fake]),
    ).dict()

    to_encode.update({"user_name": "Fake"})
    return jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")


def generate_valid_token(
    realm: str, client: str = Azp.test, user_name: Optional[str] = None
) -> str:
    """
    Generate a valid token

    :param realm: realm access role
    :param client: app client
    :param user_name: app username
    :return: token
    """
    to_encode = Token(
        exp=datetime.utcnow() + timedelta(seconds=300),
        iat=datetime.utcnow(),
        azp=client,
        realm_access=Roles(roles=[RolesEnum(realm)]),
    ).dict()
    if user_name:
        to_encode.update({"user_name": user_name})

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")
