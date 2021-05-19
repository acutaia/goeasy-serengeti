#!/usr/bin/env python3
"""
Sensor models

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
from typing import Union

# Third Party
from pydantic import Field

# Internal
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class SensorDataPosition(OrjsonModel):
    """Model of a sensor data"""

    x: float = Field(..., example=15.632355)
    y: float = Field(..., example=13.435356)
    z: float = Field(..., example=12.32525235)


class SensorDataOrientation(OrjsonModel):
    """Model of a sensor data"""

    azimut: float = Field(..., example=1.632355)
    pitch: float = Field(..., example=0.435356)
    roll: float = Field(..., example=1.32525235)


class SensorInformation(OrjsonModel):
    """Model of sensor information"""

    data: Union[SensorDataPosition, SensorDataOrientation] = Field(
        ..., description="Measurement object obtained by sensor"
    )
    name: str = Field(..., description="Sensor name", example="magnetometer")
    time: int = Field(
        ..., description="UTC timestamp expressed in ms", example=1611820537461
    )
