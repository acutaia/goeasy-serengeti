#!/usr/bin/env python3
"""
UserFeed router package

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
from datetime import datetime
import uuid

# Third Party
from fastapi import APIRouter, Body, Depends, BackgroundTasks, Request
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.user_feed import end_to_end_position_authentication, store_android_data
from ..models.user_feed.user import UserFeedInput
from ..models.security import Requester
from ..models.user_feed.response_class import Resource
from ..security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

# JWT  signature
test_auth = Signature(realm_access="Test")
user_feed_auth = Signature(realm_access="UserFeed", return_requester=True)

# Instantiate router
router = APIRouter(
    prefix="/api/v1/goeasy/authenticate",
    tags=["User"]
)


@router.post(
    "/",
    response_model=Resource,
    response_class=ORJSONResponse,
    summary="Authenticate User data and store them",
    response_description="Resource created",
)
async def authenticate(
        back_ground_tasks: BackgroundTasks,
        request: Request,
        requester: Requester = Depends(user_feed_auth),
        user_feed: UserFeedInput = Body(...)
):
    """
    Authenticate user data obtained from mobile
    """
    # Analyze requester
    if requester.client == "get_token_client" and requester.user == "goeasy_bq_library":
        source_app = "ApesMobility"
    else:
        source_app = requester.client

    # Generate an unique id for the journey
    journey_id = str(uuid.uuid4())

    # Store the data in the anonengine in the background
    back_ground_tasks.add_task(
        store_android_data,
        user_feed,
        datetime.now(),
        request.client.host,
        journey_id,
        source_app,
        requester.client,
        str(requester.user)
    )

    # Return the id of the resource
    return Resource(journey_id=journey_id)


@router.post(
    "/test",
    response_class=ORJSONResponse,
    summary="Test the authentication of User Data",
    response_description="Input with verified data",
    dependencies=[Depends(test_auth)]
)
async def authenticate_test(request: Request, user_feed: UserFeedInput = Body(...)):
    """
    Test the authentication process
    """
    return await end_to_end_position_authentication(
        user_feed=user_feed,
        timestamp=datetime.now(),
        host=request.client.host
    )
