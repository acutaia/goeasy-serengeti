#!/usr/bin/env python3
"""
Constants for mock Anonymizer http requests

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
from app.config import get_anonymizer_settings

# ---------------------------------------------------------------------------------------

SETTINGS = get_anonymizer_settings()
""" Anonymizer Settings """


URL_STORE_DATA = SETTINGS.store_data_url
""" Url to store data in the anonymizer """

URL_EXTRACT_MOBILITY = SETTINGS.get_mobility_url
""" Url to extract mobility data from the anonymizer """

URL_EXTRACT_DETAILS = SETTINGS.get_details_url
""" Url to extract details from the anonymizer """

MOCKED_RESPONSE = {"Foo": "Bar"}
""" Mocked Response """
