#!/usr/bin/env python3
"""
Galileo models

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
from typing import Optional, List

# Internal
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class UbloxAPI(OrjsonModel):
    """Model of single data from UbloxApi"""

    timestamp: int
    raw_data: Optional[str]


class UbloxAPIList(OrjsonModel):
    """Model of a list of data from UbloxApi"""

    satellite_id: int
    info: List[UbloxAPI]


class Ublox(OrjsonModel):
    """Model of a Ublox message"""

    svid: int
    raw_data: str


# --------------------------------------------------------------------------------------------
