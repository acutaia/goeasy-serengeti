#!/usr/bin/env python3
"""
Constants for mock Ublox-Api http requests

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

# Internal
from app.internals.ublox_api import SETTINGS, URL_UBLOX, URL_GALILEO

# ---------------------------------------------------------------------------------------


TIMESTAMP = 1611819619151
""" Timestamp of the message of interest"""

SvID = 12
""" Satellite id of the message of interest """

URL_GET_UBLOX = f"{URL_UBLOX['Italy']}/{SvID}/{TIMESTAMP}"
""" Url to get a ublox raw message """

URL_GET_GALILEO = f"{URL_GALILEO['Italy']}/{SvID}/{TIMESTAMP}"
""" Url to get a galileo raw message """

URL_POST_UBLOX = f"{URL_UBLOX['Italy']}"
""" Url to get a list of ublox messages """

URL_POST_GALILEO = f"{URL_GALILEO['Italy']}"
""" Url to get a list of ublox messages """

LOCATION = "Italy"
""" Location of the Ublox-Api server """


RaW_Ublox = "02133000000c00000a0102392a34c022408c238a04b389169ebc400e228044bfe80f43a8e604821235344582f90fd29628100086b197"
""" Ublox Raw Message """


RaW_Galileo = "021b05b6415009b9c96a3edc8e7500867e588f6792c86aaaaa62bc4c7f40"
""" Galileo Raw Message """

NUMBER_REQUESTED_DATA = (SETTINGS.window / SETTINGS.window_step) * 2
""" Number of data requested to Ublox-Api """
