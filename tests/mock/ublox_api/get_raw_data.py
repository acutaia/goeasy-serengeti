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
from .constants import TIMESTAMP
from ..keycloak.keycloak import correct_get_blox_token

# ----------------------------------------------------------------------------------------------


def correct_get_raw_data(m: aioresponses, url: str, raw_data: Optional[str]):
    """
    Mock the request made to Ublox-Api to obtain raw data

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """
    m.get(
        url,
        status=status.HTTP_200_OK,
        body=orjson.dumps({"timestamp": TIMESTAMP, "raw_data": raw_data}).decode(),
    )


def token_expired_get_raw_data(m: aioresponses, url: str, raw_data: Optional[str]):
    """
    Mock the behaviour in case of token expired

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :param raw_data: data that we want to receive
    :return:
    """

    correct_get_blox_token(m)
    m.get(url, status=status.HTTP_401_UNAUTHORIZED)
    m.get(
        url,
        status=status.HTTP_200_OK,
        body=orjson.dumps({"timestamp": TIMESTAMP, "raw_data": raw_data}).decode(),
    )


def unreachable_get_raw_data(m: aioresponses, url: str):
    """
    Mock the behaviour in case of Ublox-Api is unreachable

    :param m: aioresponses mock
    :param url: Galileo or Ublox
    :return:
    """
    m.get(url, exception=TimeoutError("Timeout"))
