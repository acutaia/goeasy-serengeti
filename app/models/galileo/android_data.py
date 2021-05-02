#!/usr/bin/env python3
"""
Galileo models

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

# --------------------------------------------------------------------------------------------


class AndroidData(str):
    """AndroidData validation"""

    @classmethod
    def __get_validators__(cls):
        """Validate the AndroidData"""
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return cls(v)

        if not isinstance(v, list):
            raise TypeError("list of int required")
        if len(v) != 30:
            raise ValueError("invalid number of elements in the list")
        try:
            # Convert in bytes
            m = b"".join(
                [
                    int(element).to_bytes(1, byteorder="big", signed=True)
                    for element in v
                ]
            ).hex()
        except ValueError as error:
            raise ValueError(error.args)
        return cls(m)


# --------------------------------------------------------------------------------------------
