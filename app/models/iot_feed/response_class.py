#!/usr/bin/env python3
"""
Response_class

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
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Resource(OrjsonModel):
    """Resource Model"""

    resource_type: str = Field(
        default="PROTECTED SERENGETI",
        title="Resource type",
    )
    url: str = Field(
        default="https://galileocloud.goeasyproject.eu/serengeti/api/v1/goeasy/IoTauthenticate",
        description="Url of the resource",
    )
    method: str = Field(default="POST")
    status: str = Field(default="correct")
    observationGEPid: str = Field(
        description="Id of the observation",
        example="9d007657-fe13-4bd7-ba3c-d609b110014a",
    )
