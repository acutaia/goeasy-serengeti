#!/usr/bin/env python3
"""
Behaviour models package

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
from typing import List, Optional

# Third Party
from pydantic import Field

# Internal
from ..track import TrackSegmentsOutput
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Behaviour(OrjsonModel):
    """User Behaviour"""
    app_defined: List[Optional[TrackSegmentsOutput]] = Field(
        ...,
        title="Application Defined Behaviour",
        description="Mobile application standalone detection of mobility types and the segments within the journey",
        example=[]
    )
    tpv_defined: List[Optional[TrackSegmentsOutput]] = Field(
        ...,
        title="Third Party Defined Behaviour",
        description="Autonomous detection of mobility types and the segments within the journey",
        example=[]
    )
    user_defined: List[Optional[TrackSegmentsOutput]] = Field(
        ...,
        title="User Defined Behaviour",
        description="""The users specify through the mobile app the type of mobility
                    (necessary to produce legitimate data to be used for the learning process of the third-party system)
                    """
    )
