#!/usr/bin/env python3
"""
IoTFeed router package

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
import uuid
from datetime import datetime

# Third Party
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import ORJSONResponse

# Internal
from ..models.iot_feed.iot import IotInput
from ..models.security import Requester
from ..security.jwt_bearer import Signature
from ..internals.iot import end_to_end_position_authentication

# --------------------------------------------------------------------------------------------

# JWT Signature
iot_auth = Signature(realm_access="IoTFeed", return_requester=True)

# Instantiate router
router = APIRouter(
    prefix="/api/v1/goeasy/IoTauthenticate",
    tags=["IoT"]
)


@router.post(
    "",
    response_class=ORJSONResponse,
    summary="Validate data from IoT devices",
)
async def iot_authentication(
        request: Request,
        requester: Requester = Depends(iot_auth),
        iot_input: IotInput = Body(...)
):
    """Checks if every position is authentic"""

    # Analyze requester
    if requester.client == "get_token_client" and requester.user == "goeasy_bq_library":
        source_app = "ApesMobility"
    else:
        source_app = requester.client

    # Generate GEPid
    obesrvation_gepid = uuid.uuid4()

    return await end_to_end_position_authentication(
        iot_input,
        datetime.now(),
        request.client.host,
        source_app,
        requester.client,
        str(requester.user),
        str(obesrvation_gepid)
    )

