#!/usr/bin/env python3
"""
Result models

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
from typing import Literal

# Third Party
from pydantic import Field

# Internal
from .point import Point
from ..security import Authenticity
from ..model import OrjsonModel
from ..galileo.gnss import Gnss

# --------------------------------------------------------------------------------------------


class Response(OrjsonModel):
    """
    Telemetry
    """

    value: float = Field(..., description="Value sensed", example=6.8)


class Result(OrjsonModel):
    """
    Result of the measurement
    """

    valueType: Literal["NO2"] = Field(
        ..., title="NO2", description="Type of measurement", example="NO2"
    )
    Position: Point = Field(..., description="Position where the measurement occurred")
    response: Response = Field(..., description="Measurement")


class ResultInput(Result):
    """
    Input of the result measurement
    """

    gnss: Gnss = Field(
        ...,
        title="Gnss",
        description="Raw Galileo Navigation Message",
        example="B56202133000000C00000A0102392A34C022408C238A04B389169EBC400E228044BFE80F43A8E604821235344582F90FD29628100086B197B56202133000001800000A0602392A34C022408C238A04B389169EBC400E228044BFE80F43A8E604821235344582F90FD29628100086C2A2B56202133000001900000A0502392A34C022408C238A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F1670110086AE66B56202133000001300000A0402392A34C0223A8C230A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F167011008621C9B56202133000000F00000A0302392A34C022408C238A90B48916CFBB80133EC0433FF21043A8FD0E8092BF27458235259F1670110086A23A",
    )


class ResultOutput(Result):
    """
    Output of the result measurement
    """

    authenticity: Authenticity = Field(
        ...,
        title="Authenticity of the data",
        description="""Value | Status        | Description
                       ------| --------------|------------------------------------------------------------
                       1     | Authentic     | Input raw data are authentic
                       -1    | Unknown       | Input raw data aren't present or impossible to authenticate 
                       0     | Not Authentic | Input raw data aren't authentic""",
        example=1,
    )
