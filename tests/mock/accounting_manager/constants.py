#!/usr/bin/env python3
"""
Constants for mock Accounting Manager http requests

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

# Internal
from app.config import get_accounting_manager_settings

# -------------------------------------------------------------------------------

SETTINGS = get_accounting_manager_settings()
""" Accounting Manager Settings """

URL_GET_IOTA_USER = f"{SETTINGS.accounting_ip}{SETTINGS.accounting_get_uri}"
""" Url to extract User info from the accounting manager """

URL_STORE_IN_IOTA = f"{SETTINGS.accounting_ip}{SETTINGS.accounting_store_uri}"
""" Url to store User info in the accounting manager """
