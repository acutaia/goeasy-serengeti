"""
Constants for mock Keycloak http requests

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

# Internal
from app.internals.keycloak import get_keycloak_settings

# ---------------------------------------------------------------------------------------

SETTINGS = get_keycloak_settings()
"""Keycloak Settings"""

FAKE_TOKEN_FOR_TESTING = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFuZ2VsbyBDdXRhaWEiLCJpYXQiOjE1MTYyMzkwMjJ9.
anXoSMyh61_O4KZXlffg6-09WkXzW18lrOAbxjol6Z4"""
""" Token generated just for testing """

TOKEN_REQUEST_URL = SETTINGS.token_request_url
""" Url to request a token to keycloak"""
