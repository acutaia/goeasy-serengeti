#!/usr/bin/env python3
"""
Anonymizer mocked Http requests

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
from typing import Optional

# Third Party
from fastapi import status
from httpx import Response, RequestError
import respx

# Internal
from .constants import URL_STORE_DATA, URL_EXTRACT_MOBILITY, URL_EXTRACT_DETAILS, MOCKED_RESPONSE

# ----------------------------------------------------------------------------------------------


def correct_store_user_in_the_anonengine():
    respx.post(URL_STORE_DATA).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json=MOCKED_RESPONSE
        )
    )


def unreachable_store_user_in_the_anonengine():
    respx.post(URL_STORE_DATA).mock(side_effect=RequestError)

# ----------------------------------------------------------------------------------------------


def correct_extract_mobility(journey_id: str):
    respx.get(f"{URL_EXTRACT_MOBILITY}/{journey_id}").mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json=MOCKED_RESPONSE
        )
    )


def unreachable_extract_mobility(journey_id: str):
    respx.get(f"{URL_EXTRACT_MOBILITY}/{journey_id}").mock(side_effect=RequestError)

# ----------------------------------------------------------------------------------------------


def correct_extract_details(journey_id: str):
    respx.get(f"{URL_EXTRACT_DETAILS}/{journey_id}").mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json=MOCKED_RESPONSE
        )
    )


def unreachable_extract_details(journey_id: str):
    respx.get(f"{URL_EXTRACT_DETAILS}/{journey_id}").mock(side_effect=RequestError)
