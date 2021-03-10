#!/usr/bin/env python3
"""
Tests app.internals.position_alteration_detection module

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
from app.internals.position_alteration_detection import haversine

# -------------------------------------------------------------------------------

ROME = {
    "lat": 41.8931,
    "lon": 12.4828
}
""" Rome latitude and longitude """

STOCKHOLM = {
    "lat": 59.334591,
    "lon": 18.063240
}
""" Stockholm latitude and longitude """


def test_haversine():
    """ Test haversine"""
    assert haversine(ROME["lat"], ROME["lon"]) == "Italy", "Rome is in Italy"
    assert haversine(STOCKHOLM["lat"], STOCKHOLM["lon"]) == "Sweden", "Stockholm is in Sweden"
