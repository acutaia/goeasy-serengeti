#!/usr/bin/env python3
"""
Anonymizer package

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
from asyncio import TimeoutError
from datetime import datetime

# Third Party
from aiohttp import ClientError
from fastapi import status, HTTPException
import orjson

# Internal
from .logger import get_logger
from .sessions.accounting_manager import get_accounting_session
from ..models.accounting_manager import AccountingManager, Data, Obj
from ..config import get_accounting_manager_settings

# ----------------------------------------------------------------------------------------------------


async def get_iota_user(user: str) -> dict:
    """
    Extract user info from the accounting manager

    :param user: user of interested
    :return: user_info
    """
    # Get Logger
    logger = get_logger()

    settings = get_accounting_manager_settings()

    try:
        async with get_accounting_session() as session:
            async with session.get(
                f"{settings.accounting_ip}{settings.accounting_get_uri}",
                params={"user": user},
                timeout=20,
            ) as resp:
                return await resp.json(
                    encoding="utf-8", loads=orjson.loads, content_type=None
                )

    except (TimeoutError, ClientError) as exc:
        # Something went wrong during the connection
        await logger.warning(
            {
                "url": f"{settings.accounting_ip}{settings.accounting_get_uri}",
                "error": repr(str(exc)),
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't contact IoTa service"
        )


async def store_in_iota(
    source_app: str,
    client_id: str,
    user_id: str,
    msg_id: str,
    msg_size: int,
    msg_time: float,
    msg_malicious_position: int,
    msg_authenticated_position: int,
    msg_unknown_position: int,
    msg_total_position: int,
    msg_error: bool = False,
    msg_error_description: str = "",
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
    # Get Logger
    logger = get_logger()

    settings = get_accounting_manager_settings()

    try:
        async with get_accounting_session() as session:
            async with session.post(
                f"{settings.accounting_ip}{settings.accounting_store_uri}",
                json=AccountingManager(
                    target=f"{source_app}-{datetime.now().date()}",
                    data=Data(
                        AppObj=Obj(
                            client_id=client_id,
                            user_id=user_id,
                            msg_id=msg_id,
                            msg_size=msg_size,
                            msg_time=msg_time,
                            msg_malicious_position=msg_malicious_position,
                            msg_authenticated_position=msg_authenticated_position,
                            msg_unknown_position=msg_unknown_position,
                            msg_total_position=msg_total_position,
                            msg_error=msg_error,
                            msg_error_description=msg_error_description,
                        )
                    ),
                ).dict(),
                timeout=1,
            ):
                pass

    except (TimeoutError, ClientError) as exc:
        # Something went wrong during the connection
        await logger.warning(
            {
                "url": f"{settings.accounting_ip}{settings.accounting_get_uri}",
                "error": repr(str(exc)),
            }
        )
    finally:
        return
