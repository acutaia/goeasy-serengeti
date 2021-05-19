#!/usr/bin/env python3
"""
Constants for mock Anonymizer http requests

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

# Internal
from app.config import get_anonymizer_settings
from app.config import get_ipt_anonymizer_settings

# ---------------------------------------------------------------------------------------

SETTINGS_ANONENGINE = get_anonymizer_settings()
""" Anonengine Settings """

SETTINGS_IPT = get_ipt_anonymizer_settings()
""" IPT-Anonymizer settings """


URL_STORE_USER_DATA = SETTINGS_IPT.store_user_data_url
""" Url to store user data in the IPT-Anonymizer """

URL_STORE_IOT_DATA = SETTINGS_IPT.store_iot_data_url
""" Url to store iot data in the IPT-Anonymizer """

URL_EXTRACT_USER_DATA = SETTINGS_IPT.extract_user_data_url
""" Url to extract user data from the IPT-Anonymizer"""

URL_STORE_DATA = SETTINGS_ANONENGINE.store_data_url
""" Url to store user data in the anonengine """

URL_EXTRACT_MOBILITY = SETTINGS_ANONENGINE.get_mobility_url
""" Url to extract mobility data from the anonengine """

URL_EXTRACT_DETAILS = SETTINGS_ANONENGINE.get_details_url
""" Url to extract details from the anonengine """

MOCKED_RESPONSE = {"Foo": "Bar"}
""" Mocked Response """
