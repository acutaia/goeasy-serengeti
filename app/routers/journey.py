#!/usr/bin/env python3
"""
Journey router package

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
    """Extract mobility info from the track of interest"""
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
    """"Extract details from the track of interest"""
    return await extract_details(str(journey.journey_id))
