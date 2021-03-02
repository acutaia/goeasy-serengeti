#!/usr/bin/env python3
"""
Administrator router package

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

# Third Party
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.accounting_manager import get_iota_user
from ..models.admin import SourceApp
from ..security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

# JWT signature
admin_auth = Signature(realm_access="Administration")

# Instantiate router
router = APIRouter(
    prefix="/api/v1/goeasy/getAccounting",
    tags=["Admin"]
)


@router.post(
    "/{source_app}",
    response_class=ORJSONResponse,
    summary="Validate data from IoT devices",
    dependencies=[Depends(admin_auth)]
)
async def extract_user(source_app: SourceApp):
    """Extract User information from the accounting manager"""
    return await get_iota_user(source_app.value)

