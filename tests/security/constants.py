#!/usr/bin/env python3
"""
Constants security

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
import os

# -------------------------------------------------------------------------------------------------------------
PATH = os.path.abspath(os.path.dirname(__file__))
"""Path to the directory containing private.pem and public.pem"""

ISSUER = "Travis-ci/test"
"""Used only for CI"""

AUDIENCE = "Travis-ci/test"
"""Used only for CI"""

with open(f"{PATH}/public.pem", "r") as fp:
    PUBLIC_KEY = fp.read()
"""Public token key used for testing purpose"""

with open(f"{PATH}/private.pem", "r") as fp:
    PRIVATE_KEY = fp.read()
"""Private token key used for testing purpose"""
