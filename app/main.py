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
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse

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


# Documentation end-point
@app.get("/api/v1/galileo/docs", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Serengeti",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/satellite.png",
    )


@app.post(
    "/api/v1/goeasy/statistics",
    response_class=ORJSONResponse,
)
async def get_statistics(
        realm_access_roles: List[str] = Depends(extraction_auth),
        extraction: InputJSONExtraction = Body(...),
):
    """"Extract statistics info"""

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

    raise status.HTTP_425_TOO_EARLY


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
        "url": "/static/logo_full.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Substitute the docs with the custom one
app.openapi = custom_openapi