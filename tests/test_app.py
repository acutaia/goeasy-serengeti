#!/usr/bin/env python3
"""
Test app

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
# Standard library
import uuid

# Test
from aioresponses import aioresponses
from fastapi.testclient import TestClient
import pytest
import respx

# Third Party
import orjson
from fastapi import status

# Internal
from app.main import app
from app.models.admin import SourceApp
from app.internals.sessions.ublox_api import get_ublox_api_session
from app.internals.sessions.anonymizer import get_anonengine_session
from app.internals.sessions.ipt_anonymizer import get_ipt_anonymizer_session
from app.internals.sessions.accounting_manager import get_accounting_session

from .internals.iot.constants import IOT_INPUT_PATH
from .internals.logger import disable_logger
from .internals.user_feed.constants import USER_INPUT_PATH
from .security.model import Azp, UserName, RolesEnum
from .security.token import (
    change_default_security_settings,
    generate_fake_token,
    generate_valid_token,
)
from .mock.keycloack.keycloack import correct_get_blox_token
from .mock.accounting_manager.iota import correct_get_iota_user, correct_store_in_iota
from .mock.anonymizer.anonengine import (
    correct_extract_details,
    correct_extract_mobility,
    correct_store_user_in_the_anonengine,
)
from .mock.anonymizer.constants import URL_STORE_IOT_DATA, URL_STORE_USER_DATA
from .mock.anonymizer.ipt import correct_store_in_ipt_anonymizer
from .mock.ublox_api.constants import (
    RaW_Ublox,
    RaW_Galileo,
    URL_GET_UBLOX,
    URL_GET_GALILEO,
)
from .mock.ublox_api.get_raw_data import correct_get_raw_data

# ---------------------------------------------------------------------------------------------


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


def clear_test():
    """Clear tests"""
    disable_logger()
    change_default_security_settings()
    get_ublox_api_session.cache_clear()
    get_anonengine_session.cache_clear()
    get_accounting_session.cache_clear()
    get_ipt_anonymizer_session.cache_clear()


def test_docs_and_startup_shutdown(mock_aioresponse):
    """Test docs and startup and shutdown events"""

    # Load the cache of the documentation
    app.openapi_schema = None
    app.openapi()
    app.openapi()

    correct_get_blox_token(mock_aioresponse)

    with TestClient(app) as client:
        response = client.get("/api/v1/docs")
        assert response.status_code == 200

    clear_test()


class TestAdmin:
    """Test administrator router"""

    @respx.mock
    def test_administrator(self, mock_aioresponse):
        """Test the behaviour of administrator router"""

        clear_test()
        correct_get_iota_user(mock_aioresponse, user=SourceApp.any)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token = generate_valid_token(realm=RolesEnum.admin)
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        correct_get_blox_token(mock_aioresponse)

        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                f"http://serengeti/api/v1/goeasy/getAccounting/{SourceApp.any}",
                headers={"Authorization": f"Bearer {invalid_token}"},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                f"http://serengeti/api/v1/goeasy/getAccounting/{SourceApp.any}",
                headers={"Authorization": invalid_token},
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Try to use a valid token but without the requested role
            response = client.post(
                f"http://serengeti/api/v1/goeasy/getAccounting/{SourceApp.any}",
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Use a valid token
            response = client.post(
                f"http://serengeti/api/v1/goeasy/getAccounting/{SourceApp.any}",
                headers={"Authorization": f"Bearer {valid_token}"},
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've mocked the request

        clear_test()


class TestIoT:
    """Test IoT router"""

    @respx.mock
    def test_iot_authentication(self, mock_aioresponse):
        """Test the behaviour of  iot authentication endpoint"""

        # Setup
        clear_test()
        with open(IOT_INPUT_PATH, "r") as fp:
            IOT_INPUT = orjson.loads(fp.read())

        # Mock the request
        correct_get_blox_token(mock_aioresponse)
        correct_get_raw_data(mock_aioresponse, url=URL_GET_UBLOX, raw_data=RaW_Ublox)
        correct_store_in_iota(mock_aioresponse)
        correct_store_in_ipt_anonymizer(mock_aioresponse, URL_STORE_IOT_DATA)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token_requester_test = generate_valid_token(realm=RolesEnum.iot)
        valid_token_requester_apes_mobility = generate_valid_token(
            realm=RolesEnum.iot,
            client=Azp.get_token_client,
            user_name=UserName.goeasy_bq_library,
        )
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={"Authorization": f"Bearer {invalid_token}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use a valid token but without the requested role
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={"Authorization": f"FAKE {invalid_token}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Use a valid token with the requester set to test
            response = client.post(
                f"http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={"Authorization": f"Bearer {valid_token_requester_test}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with the requester set to apes_mobility
            response = client.post(
                f"http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={
                    "Authorization": f"Bearer {valid_token_requester_apes_mobility}"
                },
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with a wrong body
            response = client.post(
                f"http://serengeti/api/v1/goeasy/IoTauthenticate",
                headers={
                    "Authorization": f"Bearer {valid_token_requester_apes_mobility}"
                },
                json={"Wrong": "Body"},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        clear_test()

    @respx.mock
    def test_authenticate_test(self, mock_aioresponse):
        """Test the behaviour of  iot authentication endpoint"""

        # Setup
        clear_test()
        with open(IOT_INPUT_PATH, "r") as fp:
            IOT_INPUT = orjson.loads(fp.read())

        # Mock the request
        correct_get_blox_token(mock_aioresponse)
        correct_get_raw_data(mock_aioresponse, url=URL_GET_UBLOX, raw_data=RaW_Ublox)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token = generate_valid_token(realm=RolesEnum.test)
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate/test",
                headers={"Authorization": f"Bearer {invalid_token}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use a valid token but without the requested role
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate/test",
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate/test",
                headers={"Authorization": f"FAKE {invalid_token}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Use a valid token with the requester set to test
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate/test",
                headers={"Authorization": f"Bearer {valid_token}"},
                json=IOT_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with a wrong body
            response = client.post(
                "http://serengeti/api/v1/goeasy/IoTauthenticate/test",
                headers={"Authorization": f"Bearer {valid_token}"},
                json={"Wrong": "Body"},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        clear_test()


class TestJourney:
    """Test Journey Router"""

    @staticmethod
    def setup() -> str:
        clear_test()
        return str(uuid.uuid4())

    @staticmethod
    def journey_analysis(
        journey_id: str,
        url: str,
        invalid_token: str,
        valid_token: str,
        valid_token_role_not_present: str,
        mocked: aioresponses,
    ):
        """
        Inner function used to test both endpoints
        """
        correct_get_blox_token(mocked)
        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                url=url,
                headers={"Authorization": f"Bearer {invalid_token}"},
                json={"journey_id": journey_id},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use a valid token but without the requested role
            response = client.post(
                url=url,
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
                json={"journey_id": journey_id},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                url=url,
                headers={"Authorization": invalid_token},
                json={"journey_id": journey_id},
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Use a valid token
            response = client.post(
                url=url,
                headers={"Authorization": f"Bearer {valid_token}"},
                json={"journey_id": journey_id},
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested the extract mobility

            # Use a valid token with a wrong body
            response = client.post(
                url=url,
                headers={"Authorization": f"Bearer {valid_token}"},
                json={"Wrong": "Body"},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        clear_test()

    @respx.mock
    def test_get_mobility(self, mock_aioresponse):
        """Test the behaviour of get_mobility endpoint"""

        # Setup
        journey_id = TestJourney.setup()

        # Mock the request
        correct_extract_mobility(mock_aioresponse, journey_id=journey_id)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token = generate_valid_token(realm=RolesEnum.inspect)
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        # Test
        TestJourney.journey_analysis(
            journey_id=journey_id,
            url="http://serengeti/api/v1/goeasy/getMobility",
            invalid_token=invalid_token,
            valid_token=valid_token,
            valid_token_role_not_present=valid_token_role_not_present,
            mocked=mock_aioresponse,
        )

    @respx.mock
    def test_get_details(self, mock_aioresponse):
        """Test the behaviour of get_details endpoint"""

        # Setup
        journey_id = TestJourney.setup()

        # Mock the request
        correct_extract_details(mock_aioresponse, journey_id=journey_id)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token = generate_valid_token(realm=RolesEnum.extract)
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        # Test
        TestJourney.journey_analysis(
            journey_id=journey_id,
            url="http://serengeti/api/v1/goeasy/getDetails",
            invalid_token=invalid_token,
            valid_token=valid_token,
            valid_token_role_not_present=valid_token_role_not_present,
            mocked=mock_aioresponse,
        )


class TestUser:
    """Test User router"""

    @respx.mock
    def test_authenticate_test(self, mock_aioresponse):
        """Test the behaviour of  iot authentication endpoint"""

        # Setup
        clear_test()
        with open(USER_INPUT_PATH, "r") as fp:
            USER_INPUT = orjson.loads(fp.read())

        # Mock the request
        correct_get_blox_token(mock_aioresponse)
        correct_get_raw_data(
            mock_aioresponse, url=URL_GET_GALILEO, raw_data=RaW_Galileo
        )

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token = generate_valid_token(realm=RolesEnum.test)
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate/test",
                headers={"Authorization": f"Bearer {invalid_token}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use a valid token but without the requested role
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate/test",
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate/test",
                headers={"Authorization": f"FAKE {invalid_token}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Use a valid token with the requester set to test
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate/test",
                headers={"Authorization": f"Bearer {valid_token}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with a wrong body
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate/test",
                headers={"Authorization": f"Bearer {valid_token}"},
                json={"Wrong": "Body"},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        clear_test()

    @respx.mock
    def test_authenticate(self, mock_aioresponse):
        """Test the behaviour of the authenticate endpoint"""

        # Setup
        clear_test()
        with open(USER_INPUT_PATH, "r") as fp:
            USER_INPUT = orjson.loads(fp.read())

        # Mock the request
        correct_get_blox_token(mock_aioresponse)
        correct_get_raw_data(
            mock_aioresponse, url=URL_GET_GALILEO, raw_data=RaW_Galileo
        )
        correct_store_in_iota(mock_aioresponse)
        correct_store_user_in_the_anonengine(mock_aioresponse)
        correct_store_in_ipt_anonymizer(mock_aioresponse, URL_STORE_USER_DATA)

        # Obtain tokens
        invalid_token = generate_fake_token()
        valid_token_requester_test = generate_valid_token(realm=RolesEnum.user)
        valid_token_requester_apes_mobility = generate_valid_token(
            realm=RolesEnum.user,
            client=Azp.get_token_client,
            user_name=UserName.goeasy_bq_library,
        )
        valid_token_role_not_present = generate_valid_token(realm=RolesEnum.fake)

        with TestClient(app) as client:
            # Try to use an invalid token
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate",
                headers={"Authorization": f"Bearer {invalid_token}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use a valid token but without the requested role
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate",
                headers={"Authorization": f"Bearer {valid_token_role_not_present}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # Try to use an invalid Authorization method in the header
            response = client.post(
                "http://serengeti/api/v1/goeasy/authenticate",
                headers={"Authorization": f"FAKE {invalid_token}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

            # Use a valid token with the requester set to test
            response = client.post(
                f"http://serengeti/api/v1/goeasy/authenticate",
                headers={"Authorization": f"Bearer {valid_token_requester_test}"},
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with the requester set to apes_mobility
            response = client.post(
                f"http://serengeti/api/v1/goeasy/authenticate",
                headers={
                    "Authorization": f"Bearer {valid_token_requester_apes_mobility}"
                },
                json=USER_INPUT,
            )
            assert response.status_code == status.HTTP_200_OK
            # we don't check the response value cause we've already tested end_to_end authentication

            # Use a valid token with a wrong body
            response = client.post(
                f"http://serengeti/api/v1/goeasy/authenticate",
                headers={"Authorization": f"Bearer {valid_token_requester_test}"},
                json={"Wrong": "Body"},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        clear_test()
