#!/usr/bin/env python3
"""
Test custom data types

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

# Test
import pytest

# Third Party
from pydantic import ValidationError

# Internal
from .constants import (
    Galileo,
    Ublox,
    InputAndoidData,
    InputAndoidDataConverted,
    InputGnssData,
    InputGnssDataConverted,
    SvID,
)

# ----------------------------------------------------------------------------------------


def test_android_data():

    # Correct AndroidData
    data = Galileo(data=InputAndoidData)
    assert data.data == InputAndoidDataConverted, "Android data must be the same"
    data = Galileo(data=data.data)
    assert (
        data.data == InputAndoidDataConverted
    ), "Data already converted... must be the same"

    with pytest.raises(ValidationError):
        Galileo(data={"Invalid": "Data"})

    with pytest.raises(ValueError):
        Galileo(data=InputAndoidData.append(10))

    with pytest.raises(ValueError):
        InputAndoidData[0] = "wrong data"
        Galileo(data=InputAndoidData)

    with pytest.raises(ValueError):
        Galileo(data=["WRONG" for i in range(30)])


def test_gnss_data():

    # Correct
    data = Ublox(data=InputGnssData)
    assert data.data[0].raw_data == InputGnssDataConverted, "Raw data must be the same"
    assert data.data[0].svid == SvID, "Satellite id must be the same"

    with pytest.raises(ValidationError):
        Ublox(data={"Incorrect": "Format"})

    with pytest.raises(ValueError):
        Ublox(data="WRONG_DATA")
