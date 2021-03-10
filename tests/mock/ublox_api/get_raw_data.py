"""
Mocked Ublox Api http get requests

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
from .constants import TIMESTAMP
from .get_token import correct_get_blox_token

# ----------------------------------------------------------------------------------------------


def correct_get_raw_data(url: str, raw_data: Optional[str]):
    """
    Mock the request made to Ublox-Api to obtain raw data

    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """
    respx.get(url).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json={
                "timestamp": TIMESTAMP,
                "raw_data": raw_data
            }
        )
    )


def token_expired_get_raw_data(url: str, raw_data: Optional[str]):
    """
    Mock the behaviour in case of token expired

    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """

    correct_get_blox_token()
    route = respx.get(url)
    route.side_effect = [
        Response(
            status_code=status.HTTP_401_UNAUTHORIZED
        ),
        Response(
            status_code=status.HTTP_200_OK,
            json={
                "timestamp": TIMESTAMP,
                "raw_data": raw_data
            }
        )
    ]


def ublox_api_unreachable_get_raw_data(url: str):
    """
    Mock the behaviour in case of Ublox-Api is unreachable

    :param url: Galileo or Ublox
    :return:
    """
    respx.get(url).mock(side_effect=RequestError)





