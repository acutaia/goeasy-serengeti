#!/usr/bin/env python3
"""
GNSS model

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
from typing import List
from enum import IntEnum

# Internal
from .ublox_api import Ublox

# --------------------------------------------------------------------------------------------


class GnssID(IntEnum):
    GPS = 0
    SBAS = 1
    Galileo = 2
    Beidou = 3
    QZSS = 5
    GLONASS = 6
    ERROR = -1

# --------------------------------------------------------------------------------------------


class Gnss(List[Ublox]):
    """
    Gnss data
    """
    @classmethod
    def __get_validators__(cls):
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        field_schema.update(
            default_factory="",
            examples="B56202133000000C00000A0102392A34C022408C238A04B389169EBC400E228044BFE80F43A8E604821235344582F90FD29628100086B197B56202133000001800000A0602392A34C022408C238A04B389169EBC400E228044BFE80F43A8E604821235344582F90FD29628100086C2A2B56202133000001900000A0502392A34C022408C238A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F1670110086AE66B56202133000001300000A0402392A34C0223A8C230A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F167011008621C9B56202133000000F00000A0302392A34C022408C238A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F1670110086A23A"
        )

    @classmethod
    def validate(cls, v) -> List[Ublox]:
        if not isinstance(v, str):
            raise TypeError('string required')
        try:
            m = [
                Ublox.construct(
                    **{
                        "svid": bytes.fromhex(
                            element
                        )[5],
                        "raw_data":element
                    }
                )
                for element in v.lower().split("b562")
                if element != ""
            ]
        except ValueError:
            raise ValueError("Invalid GNSS message")

        return m
