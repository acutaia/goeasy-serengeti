#!/usr/bin/env python3
"""
jwt signature module

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

# Standard Library
from typing import List, Optional, Union

# Third Party
from aiologger.loggers.json import JsonLogger
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# Internal
from ..config import get_security_settings
from ..models.security import Requester

logger = JsonLogger.with_default_handlers(name="security", serializer_kwargs={"indent": 4})#, flatten=True)

# ----------------------------------------------------------------------------------------


class Signature(HTTPBearer):
    def __init__(self, realm_access: str, return_realm_access_list: bool = False, return_requester: bool = False):
        super().__init__()
        self.realm_access = realm_access
        self.return_realm_access_list = return_realm_access_list
        self.return_requester = return_requester

    async def __call__(self, request: Request) -> Optional[Union[List[str], Requester]]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong authentication method"
            )

        jwt_token = credentials.credentials
        settings = get_security_settings()

        try:
            token = jwt.decode(
                jwt_token,
                f"-----BEGIN PUBLIC KEY-----\n"
                f"{settings.realm_public_key}"
                f"\n-----END PUBLIC KEY-----""",
                settings.algorithm,
                issuer=settings.issuer,
                options={
                    "verify_aud": False,
                },
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_bearer_token"
            )

        # Token debug
        logger.debug(
            {
                "token_roles": token["realm_access"]["roles"]
            }
        )

        if self.realm_access not in token["realm_access"]["roles"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_bearer_token"
            )
        if self.return_realm_access_list:
            return token["realm_access"]["roles"]

        if self.return_requester:
            if "user_name" in token:
                requester = Requester(client=token["azp"], user=token["user_name"])
            else:
                requester = Requester(client=token["azp"])

            # Requester debug
            logger.debug(
                {
                    "requester_client": requester.client,
                    "requester_user": requester.user
                }
            )

            return requester
