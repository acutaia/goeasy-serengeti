#!/usr/bin/env python3
"""
IoT models

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
from datetime import datetime

# Third Party
from pydantic import Field

# Internal
from .links import DatastreamLink, FeatureOfInterestLink
from .result import ResultInput
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class IotInput(OrjsonModel):
    """
    IOTFeed input
    """

    resultTime: datetime = Field(
        ...,
        title="Result Time",
        description="The time when the result was generated",
        example="2020-10-16T09:29:43+02:00",
    )
    Datastream: DatastreamLink = Field(
        ...,
        description="Link to the OGC DataStream associated to this observation",
        example={"@iot.id": 5},
    )

    FeatureOfInterest: FeatureOfInterestLink = Field(
        ...,
        title="Feature Of Interest",
        description="Link to the OGC FeatureOfInterest associated to this observation",
        example={"@iot.id": "1"},
    )
    phenomenonTime: datetime = Field(
        ...,
        title="Phenomenon Time",
        description="The time when the result was generated",
        example="2020-10-16T09:29:43+02:00",
    )

    result: ResultInput = Field(
        ..., title="Result", description="Result of the measurement"
    )
