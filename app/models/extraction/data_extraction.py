#!/usr/bin/env python3
"""
Data Extraction models

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

# Third Party
from pydantic import Field

# Internal
from ..track import RequestType, DetectionType, MobilityType, AggregationType, TypeDay, TypeOfTrack
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class InputJSONExtraction(OrjsonModel):
    request: RequestType = Field(
        ...,
        description="Typology of request",
        example="Partial_Mobility"
    )
    start_time: int = Field(
        ...,
        description="Starting time in ms",
        example=1611819579051
    )
    start_time_high_threshold: int = Field(
        ...,
        description="Right boundary of the starting time",
        example=3600_000
    )
    start_lat: float = Field(
        description="Starting latitude",
        example=5.74235
    )
    start_lon: float = Field(
        description="Starting longitude",
        example=14.45236
    )
    start_radius: float = Field(
        description="Starting radius with specified center in meters",
        example=123.35161
    )
    end_time: int = Field(
        ...,
        description="Ending time in ms",
        example=1611819589051
    )
    end_time_high_threshold: str = Field(
        ...,
        description="Right boundary of the ending time",
        example=3600_000
    )
    end_lat: float = Field(
        description="Ending latitude",
        example=16.45236
    )
    end_lon: float = Field(
        description="Ending longitude",
        example=4.45236
    )
    end_radius: float = Field(
        description="Ending radius with specified center in meters",
        example=146.45236
    )
    type_day: TypeDay = Field(
        description="Interest type of day",
        example="Week_End"
    )
    type_detection: DetectionType = Field(
    )
    type_mobility: MobilityType = Field(
    )
    company_code: str = Field(
        description="Permit the extraction of company related data"
    )
    company_trip_type: TypeOfTrack = Field(
    )
    type_aggregation: AggregationType = Field(
        example="time"
    )
    value_aggregation: int = Field(
        description="Amounts of time in minutes or space in Km",
        example=10
    )

