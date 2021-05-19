"""
Link Models

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

# Standard Library
from typing import TypeVar, Dict, Literal

# --------------------------------------------------------------------------------------------


DatastreamLink = TypeVar("DatastreamLink", bound=Dict[Literal["@iot.id"], int])
"""Link to the OGC DataStream"""

FeatureOfInterestLink = TypeVar(
    "FeatureOfInterestLink", bound=Dict[Literal["@iot.id"], str]
)
"""Link to the OGC FeatureOfInterest"""
