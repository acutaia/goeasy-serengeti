"""
App main entry point

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0

..

    Copyright 2021 LINKS Foundation

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

# Third Party
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

# Internal
from .internals.logger import get_logger
from .internals.keycloak import KEYCLOAK
from .routers import user_feed, journey, iot, administrator, statistics

# --------------------------------------------------------------------------------------------

# Instantiate app
app = FastAPI(root_path="/serengeti", docs_url=None, redoc_url=None)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(user_feed.router)
app.include_router(journey.router)
app.include_router(iot.router)
app.include_router(administrator.router)
app.include_router(statistics.router)


# Configure logger
@app.on_event("startup")
async def startup_logger_and_sessions():
    get_logger()
    await KEYCLOAK.setup()


# Shutdown logger
@app.on_event("shutdown")
async def shutdown_logger_and_sessions():
    logger = get_logger()
    await KEYCLOAK.close()
    await logger.shutdown()


# Documentation end-point
@app.get("/api/v1/docs", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=f"/serengeti{app.openapi_url}",
        title="Serengeti",
        redoc_js_url="/serengeti/static/redoc.standalone.js",
        redoc_favicon_url="/serengeti/static/satellite.png",
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
    openapi_schema["info"]["x-logo"] = {"url": "/serengeti/static/logo_full.png"}
    openapi_schema["servers"] = [{"url": app.root_path}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Substitute the docs with the custom one
app.openapi = custom_openapi
