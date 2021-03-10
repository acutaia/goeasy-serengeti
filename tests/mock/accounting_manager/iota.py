#!/usr/bin/env python3
"""
Mocked IoTa requests

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
from .constants import URL_GET_IOTA_USER, URL_STORE_IN_IOTA

# -------------------------------------------------------------------------------


def correct_get_iota_user(user: str):
    """ Mocked get iota user """
    respx.get(URL_GET_IOTA_USER).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json={
                "user": user
            }
        )
    )


def unreachable_get_iota_user():
    """ Mocked get iota user """
    respx.get(URL_GET_IOTA_USER).mock(side_effect=RequestError)

# -------------------------------------------------------------------------------


def correct_store_in_iota():
    """ Mocked store in iota """
    respx.post(URL_STORE_IN_IOTA).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK
        )
    )


def unreachable_store_in_iota():
    """ Mocked store in iota """
    respx.post(URL_STORE_IN_IOTA).mock(side_effect=RequestError)
