#!/usr/bin/env python3
"""
Accounting Manager model

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
from datetime import datetime

# Internal
from .model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Obj(OrjsonModel):
    client_id: str
    user_id: str
    msg_id: str
    msg_size: int
    msg_time: datetime
    msg_malicious_position: int
    msg_authenticated_position: int
    msg_unknown_position: int
    msg_total_position: int
    msg_error: bool
    msg_error_description: str


class Data(OrjsonModel):
    AppObj: Obj


class AccountingManager(OrjsonModel):
    target: str
    data: Data
    private: bool = True


# --------------------------------------------------------------------------------------------
