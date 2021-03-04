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
import time

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
    """
    This endpoint provides a unique point of access to let IoT devices and LBS applications to send standardized
    data through a JSON payload via https POST requests.\n
    It enables the authentication of positions collected by third-party applications.\n
    After the security framework approval, it responds by embedding a unique, random, and anonymous id,
    generated on the cloud, for the specific track provided.\n
    Finally, the content of the message received is parsed and sanitized.\n
    The logic developed enables the reception of a set of locations embedding Galileo raw data.\n
    It requires the presence of the entire Galileo navigation messages received while the
    external devices were computing their positions.\n
    The latitude and longitude of the list of positions received are
    extracted at run-time by the Reference System Manager library
    and exploited for the proper selection of the U-Blox Reference System instance.
    """

    # Analyze requester
    if requester.client == "get_token_client" and requester.user == "goeasy_bq_library":
        source_app = "ApesMobility"
    else:
        source_app = requester.client

    # Generate GEPid
    obesrvation_gepid = uuid.uuid4()

    return await end_to_end_position_authentication(
        iot_input,
        time.time(),
        request.client.host,
        source_app,
        requester.client,
        str(requester.user),
        str(obesrvation_gepid)
    )

