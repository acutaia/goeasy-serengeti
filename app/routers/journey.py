#!/usr/bin/env python3
"""
Journey router package

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

# Third Party
from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.anonymizer import extract_details, extract_mobility
from ..models.journey.inspection import DataInspection
from ..models.journey.response_class import Resource
from ..security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

# JWT Signature
inspect_auth = Signature(realm_access="Inspect")
extraction_auth = Signature(realm_access="Extraction")

# Instantiate router
router = APIRouter(
    prefix="/api/v1/goeasy",
    tags=["Journey"]
)


@router.post(
    "/getMobility",
    response_class=ORJSONResponse,
    response_model=Resource,
    summary="Extract from the anonengine the mobility information associated to the requested journey",
    response_description="Journey Mobility Information",
    dependencies=[Depends(inspect_auth)]
)
async def get_mobility(journey: DataInspection = Body(...)):
    """
    This endpoint provides ways to let external users and applications to request for mobility
    behaviour detection information with respect to a given track id.\n
    After the security framework approval, it parses and sanitize the provided input,
    forward the request within the Federated API provided by the Privacy Aware DBMS system.\n
    The quoted system asynchronously oversees the update of the latest entries collected on the Public Database
    with the features provided by the Dependable LBS components and the mobility behaviour detection system.\n
    The values returned by the Data Access Manager are given back to the user through the https response
    within the timeout threshold of the standard.\n
    The following diagram shows the final software design of the Mobility Behaviour Detection service.\n
    ![image](https:/serengeti/static/get_mobility.png)
    """
    journey_id = str(journey.journey_id)
    mobility = await extract_mobility(journey_id)
    return Resource(journey_id=journey_id, mobility=mobility)


@router.post(
    "/getDetails",
    response_class=ORJSONResponse,
    summary="Extract from the anonengine the details associated to the requested journey",
    response_description="Journey Details",
    dependencies=[Depends(extraction_auth)]
)
async def get_details(journey: DataInspection = Body(...)):
    """
    This endpoint provides ways to let external users and applications to request,
    by specifing the id of the data of interest, the overall information collected on the platform.
    """
    return await extract_details(str(journey.journey_id))
