#!/usr/bin/env python3
"""
IPT-anonymizer session package

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2020 Angelo Cutaia

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

# Standard Library
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

# Third Party
from aiohttp import ClientTimeout, ClientSession, TCPConnector
import orjson

# ----------------------------------------------------------------------------


@dataclass(repr=False, eq=False)
class IptAnonymizerSession:
    store: ClientSession
    extract: ClientSession

    @classmethod
    def setup(cls) -> IptAnonymizerSession:
        """Setup the session"""
        store_timeout = ClientTimeout(total=60)
        store_connector = TCPConnector(limit_per_host=10, ssl=False, ttl_dns_cache=300)
        extract_timeout = ClientTimeout(total=60)
        extract_connector = TCPConnector(
            limit_per_host=20, ssl=False, ttl_dns_cache=300
        )
        self = IptAnonymizerSession(
            store=ClientSession(
                connector=store_connector,
                timeout=store_timeout,
                json_serialize=lambda x: orjson.dumps(x).decode(),
                raise_for_status=True,
                connector_owner=True,
            ),
            extract=ClientSession(
                connector=extract_connector,
                timeout=extract_timeout,
                json_serialize=lambda x: orjson.dumps(x).decode(),
                raise_for_status=True,
                connector_owner=True,
            ),
        )
        return self


@lru_cache(maxsize=1)
def get_ipt_anonymizer_session() -> IptAnonymizerSession:
    """Instantiate a IptAnonymizerSession"""
    return IptAnonymizerSession.setup()


@lru_cache(maxsize=1)
def store_session() -> ClientSession:
    """Store in the anonymizer session"""
    return get_ipt_anonymizer_session().store


@lru_cache(maxsize=1)
def extract_session() -> ClientSession:
    """Extract data from the anonymizer session"""
    return get_ipt_anonymizer_session().extract
