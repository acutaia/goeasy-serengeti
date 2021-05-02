#!/usr/bin/env python3
"""
App Settings

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
from functools import lru_cache

# Third Party
from pydantic import BaseSettings

# -------------------------------------------------------------------


class SecuritySettings(BaseSettings):
    algorithm: str
    issuer: str
    audience: str
    realm_public_key: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_security_settings() -> SecuritySettings:
    return SecuritySettings()


# -------------------------------------------------------------------


class KeycloakSettings(BaseSettings):
    token_request_url: str
    client_id: str
    username_keycloak: str
    password: str
    grant_type: str
    client_secret: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_keycloak_settings() -> KeycloakSettings:
    return KeycloakSettings()


# -------------------------------------------------------------------


class UbloxApiSettings(BaseSettings):
    meaconing_threshold: int
    ublox_api_italy_ip: str
    ublox_api_sweden_ip: str
    ublox_api_ublox_uri: str
    ublox_api_galileo_uri: str
    window: int
    window_step: int

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_ublox_api_settings() -> UbloxApiSettings:
    return UbloxApiSettings()


# -------------------------------------------------------------------


class IptAnonymizerSettings(BaseSettings):
    store_user_data_url: str
    store_iot_data_url: str
    extract_user_data_url: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_ipt_anonymizer_settings() -> IptAnonymizerSettings:
    return IptAnonymizerSettings()


class AnonymizerSettings(BaseSettings):
    get_mobility_url: str
    get_details_url: str
    store_data_url: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_anonymizer_settings() -> AnonymizerSettings:
    return AnonymizerSettings()


# -------------------------------------------------------------------


class AccountingManagerSettings(BaseSettings):
    accounting_ip: str
    accounting_get_uri: str
    accounting_store_uri: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_accounting_manager_settings() -> AccountingManagerSettings:
    return AccountingManagerSettings()


# -------------------------------------------------------------------


class LoggerSettings(BaseSettings):
    log_level: str

    class Config:
        env_file = ".env"
