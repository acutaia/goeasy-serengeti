"""
Mocked Ublox Api http post requests

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

# Standard Library
from asyncio import TimeoutError
from typing import Optional

# Third Party
from aioresponses import aioresponses
from fastapi import status
import orjson

# Internal
from .constants import TIMESTAMP, SvID
from ..keycloak.keycloak import correct_get_blox_token

# ----------------------------------------------------------------------------------------------


def correct_get_ublox_api_list(m: aioresponses, url: str, raw_data: Optional[str]):
    """
    Mock the request made to obtain a list of of UbloxApi data

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """
    m.post(
        url,
        status=status.HTTP_200_OK,
        body=orjson.dumps(
            {
                "satellite_id": SvID,
                "info": [{"timestamp": TIMESTAMP, "raw_data": raw_data}],
            }
        ).decode(),
    )


def token_expired_get_ublox_api_list(
    m: aioresponses, url: str, raw_data: Optional[str]
):
    """
    Mock the behaviour in case of token expired

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """

    correct_get_blox_token(m)
    m.post(url, status=status.HTTP_401_UNAUTHORIZED)
    m.post(
        url,
        status=status.HTTP_200_OK,
        body=orjson.dumps(
            {
                "satellite_id": SvID,
                "info": [{"timestamp": TIMESTAMP, "raw_data": raw_data}],
            }
        ).decode(),
    )


def unreachable_get_ublox_api_list(m: aioresponses, url: str):
    """
    Mock the behaviour in case of Ublox-Api is unreachable

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :return:
    """
    m.post(url, exception=TimeoutError("Timeout"))
