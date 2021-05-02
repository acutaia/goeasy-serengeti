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

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
import time

# Third Party
from fastapi import APIRouter, Body, Depends, Request, BackgroundTasks
from fastapi.responses import ORJSONResponse
from fastuuid import uuid4

# Internal
from ..concurrency.background import frequency_limiter
from ..concurrency.position_authentication import store_semaphore, position_test_lock
from ..models.iot_feed.iot import IotInput
from ..models.iot_feed.response_class import Resource
from ..models.security import Requester
from ..security.jwt_bearer import Signature
from ..internals.iot import end_to_end_position_authentication, store_iot_data

# --------------------------------------------------------------------------------------------

# JWT Signature
test_auth = Signature(realm_access="Test")
iot_auth = Signature(realm_access="IoTFeed", return_requester=True)

# Instantiate router
router = APIRouter(prefix="/api/v1/goeasy/IoTauthenticate", tags=["IoT"])


@router.post(
    "",
    response_class=ORJSONResponse,
    summary="Validate data from IoT devices",
)
async def iot_authentication(
    back_ground_tasks: BackgroundTasks,
    request: Request,
    requester: Requester = Depends(iot_auth),
    iot_input: IotInput = Body(...),
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
    obesrvation_gepid = str(uuid4())

    # Wait some time before adding the background task
    await frequency_limiter(store_semaphore())

    back_ground_tasks.add_task(
        store_iot_data,
        iot_input,
        time.time(),
        request.client.host,
        obesrvation_gepid,
        source_app,
        requester.client,
        requester.user,
        store_semaphore(),
    )
    return Resource(observationGEPid=obesrvation_gepid)


@router.post(
    "/test",
    response_class=ORJSONResponse,
    summary="Test the authentication of User Data",
    response_description="Input with verified data",
    dependencies=[Depends(test_auth)],
)
async def authenticate_test(request: Request, iot_feed: IotInput = Body(...)):
    """
    This endpoint provides ways to let users and applications to request for position data authentication services
    without the exploitation of other GEP features, such as the persistent collection.\n
    The current feature is enabled for testing purposes and for those scenarios where data is already stored on
    the cloud, and the main interests are linked on providing additional information for data trustiness.\n
    The following diagram shows the final software design of the authentication service.\n
    ![image](https:/serengeti/static/user_feed_authenticate_test.png)
    """

    # Get a semaphore to synchronize this request and prevent starvation
    async with position_test_lock():
        iot_feed_test = await end_to_end_position_authentication(
            iot_input=iot_feed,
            timestamp=time.time(),
            host=request.client.host,
        )
    return iot_feed_test
