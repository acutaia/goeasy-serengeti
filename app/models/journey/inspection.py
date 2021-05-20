"""
Data Inspection models

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
from pydantic import Field, UUID4

# Internal
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class DataInspection(OrjsonModel):
    """Data inspection model"""

    journey_id: UUID4 = Field(
        ...,
        description="Id of the track of interest",
        example="814eff18-fbf8-4a3e-81d9-670bd987ff3e",
    )


# --------------------------------------------------------------------------------------------
