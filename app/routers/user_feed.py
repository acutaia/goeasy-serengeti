#!/usr/bin/env python3
"""
UserFeed router package

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
import time
import uuid

# Third Party
from fastapi import APIRouter, Body, Depends, BackgroundTasks, Request
from fastapi.responses import ORJSONResponse

# Internal
from ..concurrency.background import frequency_limiter
from ..concurrency.position_authentication import position_test_lock, store_semaphore
from ..internals.user_feed import end_to_end_position_authentication, store_android_data
from ..models.user_feed.user import UserFeedInput, UserFeedOutput, PositionObject
from ..models.security import Requester
from ..models.user_feed.response_class import Resource
from ..security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

# JWT  signature
test_auth = Signature(realm_access="Test")
user_feed_auth = Signature(realm_access="UserFeed", return_requester=True)

# Instantiate router
router = APIRouter(prefix="/api/v1/goeasy/authenticate", tags=["User"])


@router.post(
    "",
    response_model=Resource,
    response_class=ORJSONResponse,
    summary="Authenticate User data and store them",
    response_description="Resource created",
)
async def authenticate(
    back_ground_tasks: BackgroundTasks,
    request: Request,
    requester: Requester = Depends(user_feed_auth),
    user_feed: UserFeedInput = Body(...),
):
    """
    This endpoint provides a unique point of access to let external users and applications to send standardized data
    through a JSON payload via https POST requests.
    It enables the authentication of positions collected by third-party applications.\n
    After the security framework approval, it responds by embedding a unique, random, and anonymous id,
    generated on the cloud, for the specific track provided. Finally, the content of the message received
    is parsed and sanitized.\n
    The logic developed enables the reception of a set of locations embedding Galileo raw data.
    It requires the presence of the entire Galileo navigation messages received while the external
    devices were computing their positions.\n
    The latitude and longitude of the list of positions received are extracted at run-time
    by the Reference System Manager library and exploited for the proper selection of the
    U-Blox Reference System instance.\n
    ![image](https:/serengeti/static/user_feed_authenticate.png)
    """
    # Analyze requester
    if requester.client == "get_token_client" and requester.user == "goeasy_bq_library":
        source_app = "ApesMobility"
    else:
        source_app = requester.client

    # Generate an unique id for the journey
    journey_id = str(uuid.uuid4())

    # Wait some time before adding the background task
    await frequency_limiter(store_semaphore())

    # Store the data in the anonengine in the background
    back_ground_tasks.add_task(
        store_android_data,
        user_feed,
        time.time(),
        request.client.host,
        journey_id,
        source_app,
        requester.client,
        requester.user,
        store_semaphore(),
    )

    # Return the id of the resource
    return Resource(journey_id=journey_id)


@router.post(
    "/test",
    response_class=ORJSONResponse,
    summary="Test the authentication of User Data",
    response_description="Input with verified data",
    # dependencies=[Depends(test_auth)],
)
async def authenticate_test(request: Request, user_feed: UserFeedInput = Body(...)):
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
        user_feed_test = await end_to_end_position_authentication(
            user_feed=user_feed,
            timestamp=time.time(),
            host=request.client.host,
        )

    user_feed_internal = user_feed_test.dict(
        exclude={"trace_information": {"__all__": {"galileo_auth", "galileo_status"}}}
    )
    user_feed_internal.update({"source_app": "TEST", "journey_id": "TEST"})
    return UserFeedOutput.construct(
        **{
            "app_defined_behaviour": user_feed.behaviour.app_defined,
            "tpv_defined_behaviour": user_feed.behaviour.tpv_defined,
            "user_defined_behaviour": user_feed.behaviour.user_defined,
            "company_code": user_feed.company_code,
            "company_trip_type": user_feed.company_trip_type,
            "deviceId": user_feed.id,
            "journeyId": "hello",
            "startDate": user_feed.startDate,
            "endDate": user_feed.endDate,
            "distance": user_feed.distance,
            "elapsedTime": user_feed.elapsedTime,
            "positions": [
                PositionObject.construct(
                    **{
                        "authenticity": position.authenticity,
                        "lat": position.lat,
                        "lon": position.lon,
                        "partialDistance": position.partialDistance,
                        "time": position.time,
                    }
                )
                for position in user_feed.trace_information
            ],
            "sensors": user_feed.sensors_information,
            "mainTypeSpace": user_feed.mainTypeSpace,
            "mainTypeTime": user_feed.mainTypeTime,
            "sourceApp": "TEST",
        }
    ).schema_json()
