#!/usr/bin/env python3
"""
Statistics router package

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
from typing import List

# Third Party
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.ipt_anonymizer import extract_user_info
from ..models.extraction.data_extraction import InputJSONExtraction
from ..security.jwt_bearer import Signature

# --------------------------------------------------------------------------------------------

# JWT signature
extraction_auth = Signature(realm_access="Extraction", return_realm_access_list=True)

# Instantiate router
router = APIRouter(prefix="/api/v1/goeasy/statistics", tags=["Platform"])


@router.post(
    "",
    response_class=ORJSONResponse,
    summary="Obtain statistics from the collected data",
)
async def get_statistics(
    realm_access_roles: List[str] = Depends(extraction_auth),
    extraction: InputJSONExtraction = Body(...),
):
    """
    This endpoint provides ways to let external users and applications to request for
    information collected on the platform.\n
    This interface enables external organization to gather aggregated meta-data on citizens mobility.\n
    Within the API boundaries, it is possible to parametrize requests by selecting timeframes, area of interests,
    mobility types and other details.\n
    To preserve user’s privacy, it has been defined a lower threshold for the area selected.\n
    In addition, it has been enabled the possibility to extract, with other requests,
    the list of positions for the collected journeys.\n
    Furthermore, external organization can exploit an embedded mechanism that limit the visibility
    of their data with respect to the other users enabled to interact with the platform.\n
    The following diagram shows the final software design of the data extraction service.\n
    ![image](https:/serengeti/static/get_statistics.png)
    """

    if extraction.company_code:
        if extraction.company_code not in realm_access_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
            )

    status_code, content = await extract_user_info(extraction.dict(exclude_unset=True))
    return ORJSONResponse(status_code=status_code, content=content)
