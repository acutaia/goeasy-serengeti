"""
constants for testing

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

# Third Party
from pydantic import BaseModel

# Internal
from app.models.galileo.android_data import AndroidData
from app.models.galileo.gnss import Gnss

# ----------------------------------------------------------------------------------------


class Galileo(BaseModel):
    data: AndroidData


class Ublox(BaseModel):
    data: Gnss


InputAndoidData = [
    2,
    27,
    5,
    -74,
    65,
    80,
    9,
    -71,
    -55,
    106,
    62,
    -36,
    -114,
    117,
    0,
    -122,
    126,
    88,
    -113,
    103,
    -110,
    -56,
    106,
    -86,
    -86,
    98,
    -68,
    76,
    127,
    64,
]

InputAndoidDataConverted = (
    "021b05b6415009b9c96a3edc8e7500867e588f6792c86aaaaa62bc4c7f40"
)

InputGnssData = "B56202133000000C00000A0102392A34C022408C238A04B389169EBC400E228044BFE80F43A8E604821235344582F90FD29628100086B197"

InputGnssDataConverted = "02133000000c00000a0102392a34c022408c238a04b389169ebc400e228044bfe80f43a8e604821235344582f90fd29628100086b197"

SvID = 12
