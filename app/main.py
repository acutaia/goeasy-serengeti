#!/usr/bin/env python3
"""
App main entry point

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
from fastapi import FastAPI, Body, Depends, HTTPException, status, Request
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError

# Internal
from .internals.logger import get_logger
from .routers import user_feed, journey, iot, administrator
from .models.extraction.data_extraction import InputJSONExtraction, RequestType
from .security.jwt_bearer import Signature
from .config import get_anonymizer_settings

# --------------------------------------------------------------------------------------------

extraction_auth = Signature(realm_access="Extraction", return_realm_access_list=True)

# Instantiate app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(user_feed.router)
app.include_router(journey.router)
app.include_router(iot.router)
app.include_router(administrator.router)


# Configure logger
@app.on_event("startup")
async def configure_logger():
    get_logger()


# Shutdown logger
@app.on_event("shutdown")
async def shutdown_logger():
    logger = get_logger()
    await logger.shutdown()


# Log Bad body in input
@app.exception_handler(RequestValidationError)
async def bad_request_body(request: Request, exc: RequestValidationError):
    logger = get_logger()
    await logger.debug(exc.body)
    return ORJSONResponse(
        {
            "detail": exc.errors()
        }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


# Documentation end-point
@app.get("/api/v1/docs", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=f"/serengeti/{app.openapi_url}",
        title="Serengeti",
        redoc_js_url="/serengeti/static/redoc.standalone.js",
        redoc_favicon_url="/serengeti/static/satellite.png",
    )


@app.post(
    "/api/v1/goeasy/statistics",
    response_class=ORJSONResponse,
    summary="Obtain statistics from the collected data",
    status_code=status.HTTP_425_TOO_EARLY,
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
    ![image](http:/serengeti/static/get_statistics.png)
    """

    if extraction.company_code:
        if extraction.company_code not in realm_access_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
            )
    settings = get_anonymizer_settings()

    if extraction.request == RequestType.partial_mobility:
        pass
    if extraction.request == RequestType.complete_mobility:
        pass
    if extraction.request == RequestType.all_positions:
        pass
    if extraction.request == RequestType.stats_num_tracks:
        pass
    if extraction.request == RequestType.stats_avg_time:
        pass
    if extraction.request == RequestType.stats_avg_space:
        pass

    raise HTTPException(
        status_code=status.HTTP_425_TOO_EARLY,
        detail="The endpoint is still under development"
    )


# Cache and custom documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Serengeti",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/serengeti/static/logo_full.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Substitute the docs with the custom one
app.openapi = custom_openapi
