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

# Standard Library
from typing import Optional

# Third Party
from pydantic import Field

# Internal
from ..track import (
    RequestType,
    DetectionType,
    MobilityType,
    AggregationType,
    TypeDay,
    TypeOfTrack,
)
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class InputJSONExtraction(OrjsonModel):
    request: RequestType = Field(
        ..., description="Typology of request", example="Partial_Mobility"
    )
    time_window_low: Optional[str] = Field(
        default=None, description="Left time boundary", example="08:00"
    )
    time_window_high: Optional[str] = Field(
        default=None, description="Right time boundary", example="08:15"
    )
    start_time: Optional[int] = Field(
        default=None, description="Starting time in ms", example=1611819579051
    )
    start_time_high_threshold: Optional[int] = Field(
        default=None,
        description="Right boundary of the starting time",
        example=3600_000,
    )
    start_lat: Optional[float] = Field(
        default=None, description="Starting latitude", example=5.74235
    )
    start_lon: Optional[float] = Field(
        default=None, description="Starting longitude", example=14.45236
    )
    start_radius: Optional[float] = Field(
        default=None,
        description="Starting radius with specified center in meters",
        example=123.35161,
    )
    end_time: Optional[int] = Field(
        default=None, description="Ending time in ms", example=1611819589051
    )
    end_time_high_threshold: Optional[str] = Field(
        default=None, description="Right boundary of the ending time", example=3600_000
    )
    end_lat: Optional[float] = Field(
        default=None, description="Ending latitude", example=16.45236
    )
    end_lon: Optional[float] = Field(
        default=None, description="Ending longitude", example=4.45236
    )
    end_radius: Optional[float] = Field(
        default=None,
        description="Ending radius with specified center in meters",
        example=146.45236,
    )
    type_day: Optional[TypeDay] = Field(
        default=None, description="Interest type of day", example="Week_End"
    )
    type_detection: Optional[DetectionType] = Field(
        default=None, example=DetectionType.app
    )
    type_mobility: Optional[MobilityType] = Field(
        default=None, example=MobilityType.bike
    )
    company_code: Optional[str] = Field(
        default=None, description="Permit the extraction of company related data"
    )
    company_trip_type: Optional[TypeOfTrack] = Field(
        default=None, example=TypeOfTrack.business_trip
    )
    type_aggregation: Optional[AggregationType] = Field(
        default=None, example=AggregationType.time
    )
    value_aggregation: int = Field(
        default=None,
        description="Amounts of time in minutes or space in Km",
        example=10,
    )
