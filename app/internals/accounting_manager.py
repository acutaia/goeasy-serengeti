#!/usr/bin/env python3
"""
Anonymizer package

:author: Angelo Cutaia
:copyright: Copyright 2020, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

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
from datetime import datetime

# Third Party
from aiologger.loggers.json import JsonLogger
from fastapi import status, HTTPException
import httpx
import orjson

# Internal
from ..config import get_accounting_manager_settings

logger = JsonLogger.with_default_handlers(
    name="accounting-manager",
    serializer_kwargs={"indent": 4}
)

# ----------------------------------------------------------------------------------------------------


async def get_iota_user(user: str) -> bytes:
    """
    Extract user info from the accounting manager

    :param user: user of interested
    :return: user_info
    """
    settings = get_accounting_manager_settings()

    async with httpx.AsyncClient() as client:
        try:
            response: httpx.AsyncClient() = await client.get(
                f"{settings.accounting_ip}{settings.accounting_get_uri}",
                params={"user": user}
            )
        except httpx.RequestError as exc:
            # Something went wrong during the connection
            logger.debug(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "error": exc
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Can't contact IoTa service"
            )
        return orjson.loads(response.content)


async def store_in_iota(
        source_app: str,
        client_id: str,
        user_id: str,
        msg_id: str,
        msg_size: int,
        msg_time: datetime,
        msg_malicious_position: int,
        msg_authenticated_position: int,
        msg_unknown_position: int,
        msg_total_position: int,
        msg_error: bool = False,
        msg_error_description: str = ""

) -> None:
    """
    Store info inside IoTa

    :param source_app: App that generated the data
    :param client_id: client_id expressed by the token
    :param user_id: user_id expressed by the token
    :param msg_id: uuid4
    :param msg_size: size of the output message
    :param msg_time: when the message was received
    :param msg_malicious_position: number of fake positions
    :param msg_authenticated_position: number of authentic positions
    :param msg_unknown_position: number of unknown positions
    :param msg_total_position: total number of position
    :param msg_error: error during the parsing
    :param msg_error_description: description of the error
    """

    settings = get_accounting_manager_settings()

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"{settings.accounting_ip}{settings.accounting_get_uri}",
                data=orjson.dumps(
                    {
                        "target": source_app,
                        "data": {
                            "AppObj": {
                                "client_id": client_id,
                                "user_id": str(user_id),
                                "msg_id": msg_id,
                                "msg_size": msg_size,
                                "msg_time": msg_time,
                                "msg_malicious_position": msg_malicious_position,
                                "msg_authenticated_position": msg_authenticated_position,
                                "msg_unknown_position": msg_unknown_position,
                                "msg_total_position": msg_total_position,
                                "msg_error": msg_error,
                                "msg_error_description": msg_error_description

                            }
                        },
                        "private": True
                    }
                )
            )
        except httpx.RequestError as exc:
            # Something went wrong during the connection
            logger.warning(
                {
                    "method": exc.request.method,
                    "url": exc.request.url,
                    "error": exc
                }
            )
        finally:
            return
