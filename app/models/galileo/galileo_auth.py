#!/usr/bin/env python3
"""
Galileo models

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
from pydantic import Field

# Internal
from .android_data import AndroidData
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class GalileoAuth(OrjsonModel):
    """Galileo Auth model"""

    data: AndroidData = Field(
        ...,
        title="AndroidData",
        description="Raw UBX-RXM-SFRBX payload",
        example=[
            9,
            -54,
            108,
            85,
            85,
            85,
            85,
            85,
            87,
            -62,
            0,
            80,
            55,
            -99,
            -128,
            -70,
            21,
            29,
            44,
            10,
            55,
            -119,
            -86,
            -86,
            -86,
            125,
            -72,
            35,
            127,
            64,
        ],
    )

    fullbiasnano: int = Field(
        ...,
        description="""It is the difference between hardware clock (getTimeNanos()) inside GPS receiver 
                        and the true GPS time since 0000Z, January 6, 1980, in nanoseconds""",
        example=-1295854774332368445,
    )
    msgid: int = Field(..., description="Message identifier", example=24)
    status: int = Field(
        ...,
        title="Status of RXM-SFRBX Message",
        description="""In Android the status refers to the reception of the Navigation Message with or 
                        without parity errors in its navigation words. U-blox RXM-SFRBX messages are only
                         generated when complete subframes are detected by the receiver and all appropriate
                          parity checks have passed therefore status can be set always at ‘1’""",
        example=1,
    )
    submsgid: int = Field(..., title="Sub Message ID", example=9)
    svid: int = Field(..., title="Satellite ID", example=7)
    time: int = Field(
        ..., description="UTC Unix timestamp expressed in ms", example=1611819627172
    )
    timenano: int = Field(
        ...,
        title="Clock time",
        description="GNSS receiver internal hardware clock value in nanoseconds",
        example=64668000000,
    )
    type: int = Field(
        ...,
    )
