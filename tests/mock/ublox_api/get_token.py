"""
Mocked Ublox Api http requests

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
from fastapi import status
from httpx import Response, RequestError
import respx

# Internal
from .constants import FAKE_TOKEN_FOR_TESTING, TOKEN_REQUEST_URL

# ----------------------------------------------------------------------------------------------


def correct_get_blox_token():
    """Mock the request made to keycloack to obtain a valid token"""
    respx.post(TOKEN_REQUEST_URL).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json={
                "access_token": FAKE_TOKEN_FOR_TESTING
            }
        )
    )


def unauthorized_get_ublox_token():
    """Mock the request made to keycloack to obtain a valid token"""
    respx.post(TOKEN_REQUEST_URL).mock(
        return_value=Response(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    )


def unreachable_get_ublox_token():
    """Mock the request made to keycloack to obtain a valid token"""
    respx.post(TOKEN_REQUEST_URL).mock(side_effect=RequestError)




