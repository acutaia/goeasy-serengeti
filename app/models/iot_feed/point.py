#!/usr/bin/env python3
"""
Point model

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
from typing import Literal

# Third Party
from pydantic import Field, conlist

# Internal
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Point(OrjsonModel):
    """Position description"""

    type: Literal["Point"] = Field(
        ..., title="Point", description="Position type", example="Point"
    )
    coordinate: conlist(float, min_items=2, max_items=2) = Field(
        ...,
        title="Coordinate",
        description="latitude and longitude of the point",
        example=[1.6, 7.0],
    )
