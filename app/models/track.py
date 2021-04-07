#!/usr/bin/env python3
"""
Track Models

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
from enum import Enum

# Third Party
from pydantic import Field

# Internals
from .model import OrjsonModel
from app.models.user_feed.position import PositionObjectInput, PositionObject

# --------------------------------------------------------------------------------------------


class TrackSegments(OrjsonModel):
    """ Track Segments """

    meters: int = Field(
        ...,
        example=10
    )

    type: str = Field(
        ...,
        example="walk"
    )


class TrackSegmentsInput(TrackSegments):
    """ Track Segments Input"""
    end: PositionObjectInput = Field(
        ...,
        description="End position"
    )

    start: PositionObjectInput = Field(
        ...,
        description="Start position"
    )


class TrackSegmentsOutput(TrackSegments):
    """ Track Segments Output"""
    end: PositionObject = Field(
        ...,
        description="End position"
    )

    start: PositionObject = Field(
        ...,
        description="Start position"
    )


class TypeOfTrack(str, Enum):
    """Type of track"""
    private = "private"
    commuting = "commuting"
    business_trip = "business trip"
    any = ""


class RequestType(str, Enum):
    """Track requested"""
    partial_mobility = "Partial_Mobility"
    complete_mobility = "Complete_Mobility"
    all_positions = "All_Positions"
    stats_num_tracks = "Stats_num_tracks"
    stats_avg_time = "Stats_avg_time"
    stats_avg_space = "Stats_avg_space"


class TypeDay(str, Enum):
    """Type of day"""
    working_day = "Working_Day"
    week_end = "Week_End"
    any = "Any"


class MobilityType(str, Enum):
    """Type of mobility"""
    any = "any"
    walk = "walk"
    bike = "bike"
    train = "train"
    car = "car"
    bus = "bus"
    airplane = "airplane"
    boat = "boat"


class DetectionType(str, Enum):
    """How the track was detected"""
    user = "user"
    app = "app"
    third_party = "third_party"
    any = "any"


class AggregationType(str, Enum):
    """Aggregation of the info"""
    space = "space"
    time = "time"

# --------------------------------------------------------------------------------------------



