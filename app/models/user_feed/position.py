"""
Position models

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
from typing import List, Optional

# Third Party
from pydantic import Field

# Internal
from ..security import Authenticity
from ..galileo.galileo_auth import GalileoAuth
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class PositionObject(OrjsonModel):
    authenticity: Authenticity = Field(
        ...,
        title="Authenticity of the data",
        description="""Value | Status        | Description
                       ------| --------------|------------------------------------------------------------
                         1   | Authentic     | Input raw data are authentic
                        -1   | Unknown       | Input raw data aren't present or impossible to authenticate
                         0   | Not Authentic | Input raw data aren't authentic""",
        example=1,
    )

    lat: float = Field(
        ..., title="Latitude", description="Position latitude", example=45.0700976
    )

    lon: float = Field(
        ..., title="Longitude", description="Position longitude", example=7.4728034
    )
    partialDistance: int = Field(
        ...,
        title="Partial Distance",
        description="Partial distance covered from the starting point to that position (meters)",
        example=76,
    )
    time: int = Field(..., description="UTC Unix time in ms", example=1611819579051)


class PositionObjectInput(PositionObject):
    galileo_auth: List[Optional[GalileoAuth]] = Field(..., description="Authorization")


# --------------------------------------------------------------------------------------------
