#!/usr/bin/env python3
"""
Service models

:author: Angelo Cutaia
:copyright: Copyright 2020, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

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
from typing import List

# Third Party
from pydantic import Field

# Internal
from .gnss import GnssID
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Svs(OrjsonModel):
    """Service Status Model"""
    azim: int = Field(
        ...,
        title="Azimuth",
        example=86
    )
    cno: int = Field(
        ...,
        description="Signal Strength",
        example=16
    )
    elev: int = Field(
        ...,
        title="Elevation",
        example=71
    )
    flags: int = Field(
        ...,
        example=67108864
    )
    gnssId: GnssID = Field(
        ...,
        description="""Value | Status  |
                       ------| --------|
                         0   | GPS     | 
                         1   | SBAS    |
                         2   | Galileo | 
                         3   | Beidou  | 
                         5   | QZSS    | 
                         6   | GLONASS |""",
        example=0
    )
    prRes: int = Field(
        ...,
        title="Pseudo range residual",
        example=0
    )
    svId: int = Field(
        ...,
        title="Satellite Identifier",
        example=7
    )


class SvInfo(OrjsonModel):
    """Service Status info model"""
    iTOW: int = Field(
        ...,
        description="GPS time of week of the navigation epoch",
        example=0
    )
    numSvs: int = Field(
        ...,
        description="number of per-SV data blocks",
        example=34
    )
    reserved1: int = Field(
        ...,
        description="reserved",
        example=0
    )
    svs: List[Svs] = Field(
        ...,
        description="List of service status"
    )
    version: int = Field(
        ...,
        example=0
    )

# --------------------------------------------------------------------------------------------
